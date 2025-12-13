"""
Context processors for orders app.
"""
from decimal import Decimal


def cart(request):
    """Add cart information to template context."""
    cart = request.session.get('cart', {})
    cart_count = 0
    cart_total = Decimal('0.00')
    
    for item in cart.values():
        try:
            quantity = int(item.get('quantity', 0))
            price = Decimal(str(item.get('price', 0)))
            cart_count += quantity
            cart_total += price * quantity
        except (ValueError, TypeError):
            continue
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    }

