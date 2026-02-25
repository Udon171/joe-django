from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """
    Context processor to make cart data available in every template.
    """
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    cart_total = sum(
        Decimal(item.get('price', '0')) * item.get('quantity', 0)
        for item in cart.values()
    )

    return {
        'cart_item_count': cart_count,
        'cart_total': cart_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
