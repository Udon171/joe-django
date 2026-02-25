import logging
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from gallery.models import ArtPrint
from .models import Order, OrderItem
from .utils import (
    add_to_cart, clear_cart, get_cart, get_cart_total,
    remove_from_cart, update_cart_quantity,
)

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


def cart_detail(request):
    """Display the shopping cart with all items and totals."""
    cart = get_cart(request)
    cart_items = []
    total = Decimal('0.00')

    stale_keys = []
    for pid, data in cart.items():
        try:
            art = ArtPrint.objects.get(id=pid)
            item_total = Decimal(data['price']) * data['quantity']
            total += item_total
            cart_items.append({
                'art': art,
                'quantity': data['quantity'],
                'item_total': item_total,
            })
        except ArtPrint.DoesNotExist:
            stale_keys.append(pid)

    # Clean stale items
    for key in stale_keys:
        del cart[key]
        request.session.modified = True

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/cart_detail.html', context)


@require_POST
def add_to_cart_view(request, pk):
    """Add an art print to the session cart."""
    quantity = int(request.POST.get('quantity', 1))
    try:
        add_to_cart(request, pk, quantity)
        messages.success(request, 'Item added to cart!')
    except Exception as e:
        messages.error(request, str(e))
    redirect_url = request.POST.get('redirect_url', reverse('cart_detail'))
    return redirect(redirect_url)


def remove_from_cart_view(request, pk):
    """Remove an art print from the cart."""
    remove_from_cart(request, pk)
    messages.info(request, 'Item removed from cart.')

    # Support HTMX partial update
    if request.headers.get('HX-Request'):
        return _render_cart_partial(request)
    return redirect('cart_detail')


@require_POST
def update_cart_item(request, pk):
    """Update quantity of a cart item (supports HTMX)."""
    quantity = int(request.POST.get('quantity', 1))
    update_cart_quantity(request, pk, quantity)

    if request.headers.get('HX-Request'):
        return _render_cart_partial(request)
    return redirect('cart_detail')


def _render_cart_partial(request):
    """Re-render just the cart table body for HTMX swap."""
    cart = get_cart(request)
    cart_items = []
    total = Decimal('0.00')

    for pid, data in cart.items():
        try:
            art = ArtPrint.objects.get(id=pid)
            item_total = Decimal(data['price']) * data['quantity']
            total += item_total
            cart_items.append({
                'art': art,
                'quantity': data['quantity'],
                'item_total': item_total,
            })
        except ArtPrint.DoesNotExist:
            pass

    html = render_to_string(
        'shop/includes/cart_table.html',
        {'cart_items': cart_items, 'total': total},
        request=request,
    )
    return HttpResponse(html)


@require_POST
def create_checkout_session(request):
    """Create a Stripe Checkout Session and return session ID as JSON."""
    cart = get_cart(request)
    if not cart:
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    line_items = []
    total = Decimal('0.00')

    for pid, data in cart.items():
        art = get_object_or_404(ArtPrint, id=pid)
        price_cents = int(Decimal(data['price']) * 100)
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': art.title,
                    'description': (art.description[:100]
                                    if art.description else ''),
                },
                'unit_amount': price_cents,
            },
            'quantity': data['quantity'],
        })
        total += Decimal(data['price']) * data['quantity']

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('payment_success')
            ) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('cart_detail')),
            metadata={'cart_total': str(total)},
        )

        # Create pending order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            stripe_session_id=checkout_session.id,
            total_amount=total,
        )

        for pid, data in cart.items():
            try:
                art = ArtPrint.objects.get(id=pid)
                OrderItem.objects.create(
                    order=order,
                    art_print=art,
                    quantity=data['quantity'],
                    price=Decimal(data['price']),
                )
            except ArtPrint.DoesNotExist:
                pass

        return JsonResponse({'id': checkout_session.id})

    except Exception as e:
        logger.error(f'Stripe checkout error: {e}')
        return JsonResponse({'error': str(e)}, status=400)


def payment_success(request):
    """Handle successful Stripe payment redirect."""
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                order = Order.objects.filter(
                    stripe_session_id=session_id
                ).first()
                if order and not order.is_completed:
                    order.is_completed = True
                    order.status = 'paid'
                    order.save()
                    clear_cart(request)

                    # Grant download access for logged-in users
                    if order.user and hasattr(order.user, 'profile'):
                        for item in order.items.select_related('art_print').all():
                            if item.art_print:
                                order.user.profile.purchased_prints.add(
                                    item.art_print
                                )

                    # Send confirmation email
                    _send_order_confirmation(order, session)

                    messages.success(
                        request,
                        'Payment successful! Your order is confirmed.'
                    )
        except stripe.error.StripeError as e:
            logger.error(f'Stripe verification error: {e}')
            messages.error(
                request,
                'There was an issue verifying your payment.'
            )

    return render(request, 'shop/payment_success.html')


def payment_cancel(request):
    """Handle cancelled Stripe payment."""
    messages.warning(request, 'Payment was cancelled.')
    return redirect('cart_detail')


def _send_order_confirmation(order, session):
    """Send order confirmation email after successful payment."""
    subject = 'Joe Django Art Emporium - Order Confirmation'
    message = (
        f'Thank you for your purchase!\n\n'
        f'Order #{order.id}\n'
        f'Total: \u20ac{order.total_amount:.2f}\n\n'
        f'Items:\n'
    )
    for item in order.items.select_related('art_print').all():
        title = item.art_print.title if item.art_print else 'Unknown'
        message += f'- {item.quantity} \u00d7 {title} (\u20ac{item.price})\n'
    message += (
        '\nYour digital prints are available for download '
        'in your account dashboard.'
    )

    recipient = None
    if order.user and order.user.email:
        recipient = order.user.email
    elif hasattr(session, 'customer_details') and session.customer_details:
        recipient = getattr(session.customer_details, 'email', None)

    if recipient:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f'Email send error: {e}')


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events for reliable payment processing."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if not endpoint_secret:
        logger.warning('Stripe webhook secret not configured')
        return HttpResponse(status=200)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        logger.error('Invalid webhook payload')
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError:
        logger.error('Invalid webhook signature')
        return HttpResponseBadRequest()

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order = Order.objects.filter(
            stripe_session_id=session['id']
        ).first()
        if order and not order.is_completed:
            order.is_completed = True
            order.status = 'paid'
            order.save()

            # Grant download access
            if order.user and hasattr(order.user, 'profile'):
                for item in order.items.select_related('art_print').all():
                    if item.art_print:
                        order.user.profile.purchased_prints.add(
                            item.art_print
                        )

            logger.info(f'Webhook: Payment confirmed for order {order.id}')

    return HttpResponse(status=200)


@login_required
def download_print(request, art_id):
    """Serve a purchased print file for download (protected URL)."""
    from django.http import FileResponse

    art = get_object_or_404(ArtPrint, id=art_id)
    if not request.user.profile.purchased_prints.filter(id=art.id).exists():
        messages.error(request, 'You have not purchased this print.')
        return redirect('gallery')

    if art.image:
        response = FileResponse(
            art.image.open('rb'),
            as_attachment=True,
            filename=f'{art.slug}-highres.jpg'
        )
        return response

    messages.error(request, 'Download file not available.')
    return redirect('dashboard')
