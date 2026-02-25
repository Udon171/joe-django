from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from .models import ArtPrint, Category


def gallery_list(request):
    """Display all available prints, optionally filtered by category."""
    category_slug = request.GET.get('category')
    prints = ArtPrint.objects.filter(is_available=True).select_related('category')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        prints = prints.filter(category=category)

    categories = Category.objects.all()
    context = {
        'prints': prints,
        'categories': categories,
        'active_category': category_slug,
    }
    return render(request, 'gallery/gallery_list.html', context)


def art_detail(request, slug):
    """Display a single art print with related prints."""
    art = get_object_or_404(ArtPrint, slug=slug)
    related = ArtPrint.objects.filter(
        category=art.category, is_available=True
    ).exclude(id=art.id)[:4]

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = request.user.profile.wishlist.filter(id=art.id).exists()

    context = {
        'art': art,
        'related': related,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'gallery/art_detail.html', context)


@login_required
def add_to_wishlist(request, slug):
    """Add an art print to the user's wishlist."""
    art = get_object_or_404(ArtPrint, slug=slug)
    request.user.profile.wishlist.add(art)
    messages.success(request, f'"{art.title}" added to your wishlist!')
    return redirect('art_detail', slug=slug)


@login_required
def remove_from_wishlist(request, slug):
    """Remove an art print from the user's wishlist."""
    art = get_object_or_404(ArtPrint, slug=slug)
    request.user.profile.wishlist.remove(art)
    messages.info(request, f'"{art.title}" removed from your wishlist.')
    next_url = request.GET.get('next', 'gallery')
    return redirect(next_url)
