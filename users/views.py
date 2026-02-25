from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from commissions.models import CommissionRequest
from shop.models import Order


@login_required
def dashboard(request):
    """User dashboard showing commissions, orders, and wishlist."""
    orders = Order.objects.filter(
        user=request.user, is_completed=True
    ).order_by('-created_at').prefetch_related('items__art_print')

    commissions = CommissionRequest.objects.filter(
        user=request.user
    ).order_by('-created_at')

    wishlist = request.user.profile.wishlist.all().select_related('category')
    purchased = request.user.profile.purchased_prints.all()

    context = {
        'orders': orders,
        'commissions': commissions,
        'wishlist': wishlist,
        'purchased': purchased,
    }
    return render(request, 'users/dashboard.html', context)
