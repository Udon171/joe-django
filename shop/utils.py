"""
Session-based cart utilities for the shop app.
Cart format in session: { artprint_id_str: {'quantity': int, 'price': str, 'title': str} }
"""
from decimal import Decimal
from gallery.models import ArtPrint

CART_SESSION_ID = 'cart'


def get_cart(request):
    """Returns the cart from session or creates an empty one."""
    cart = request.session.get(CART_SESSION_ID)
    if not cart:
        cart = {}
        request.session[CART_SESSION_ID] = cart
    return cart


def add_to_cart(request, artprint_id, quantity=1):
    """Add an ArtPrint to the cart or increment its quantity."""
    art = ArtPrint.objects.get(id=artprint_id)
    if not art.is_available:
        raise ValueError("This print is no longer available.")

    cart = get_cart(request)
    key = str(artprint_id)

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'quantity': quantity,
            'price': str(art.price),
            'title': art.title,
            'slug': art.slug,
        }
    request.session.modified = True


def remove_from_cart(request, artprint_id):
    """Remove an ArtPrint from the cart entirely."""
    cart = get_cart(request)
    key = str(artprint_id)
    if key in cart:
        del cart[key]
        request.session.modified = True


def update_cart_quantity(request, artprint_id, quantity):
    """Update the quantity of a cart item. Removes if quantity < 1."""
    if quantity < 1:
        remove_from_cart(request, artprint_id)
        return
    cart = get_cart(request)
    key = str(artprint_id)
    if key in cart:
        cart[key]['quantity'] = int(quantity)
        request.session.modified = True


def get_cart_total(cart):
    """Calculate the total price of all items in the cart."""
    total = Decimal('0.00')
    for item in cart.values():
        total += Decimal(item['price']) * item['quantity']
    return total


def clear_cart(request):
    """Remove the entire cart from session."""
    if CART_SESSION_ID in request.session:
        del request.session[CART_SESSION_ID]
        request.session.modified = True
