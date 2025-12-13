"""
Views for orders app - cart and order management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db import transaction
from decimal import Decimal
from products.models import Product
from .models import Order, OrderItem


def is_admin(user):
    """Check if user is an admin."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin()


def get_cart(request):
    """Get or create cart from session."""
    cart = request.session.get('cart', {})
    return cart


def save_cart(request, cart):
    """Save cart to session."""
    request.session['cart'] = cart
    request.session.modified = True


@login_required
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_cart(request)
    
    # Get quantity from request, default to 1
    quantity = int(request.GET.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    if quantity > 10:
        quantity = 10
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        cart[product_id_str] = {
            'quantity': quantity,
            'price': str(product.price),
            'name': product.name,
            'image': product.image.url if product.image else '',
        }
    
    save_cart(request, cart)
    messages.success(request, f'{product.name} added to cart!')
    
    # Redirect to previous page or cart
    next_url = request.GET.get('next', 'orders:cart')
    return redirect(next_url)


@login_required
def remove_from_cart(request, product_id):
    """Remove product from cart."""
    cart = get_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product_name = cart[product_id_str]['name']
        del cart[product_id_str]
        save_cart(request, cart)
        messages.success(request, f'{product_name} removed from cart!')
    else:
        messages.error(request, 'Product not in cart!')
    
    return redirect('orders:cart')


@login_required
def update_cart(request, product_id):
    """Update product quantity in cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_cart(request)
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            if quantity > 0:
                cart[product_id_str]['quantity'] = quantity
                save_cart(request, cart)
                messages.success(request, 'Cart updated!')
            else:
                del cart[product_id_str]
                save_cart(request, cart)
                messages.success(request, 'Item removed from cart!')
        else:
            messages.error(request, 'Product not in cart!')
    
    return redirect('orders:cart')


@login_required
def cart_view(request):
    """Display cart."""
    cart = get_cart(request)
    cart_items = []
    total = Decimal('0.00')
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            item_total = quantity * price
            total += item_total
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': item_total,
            })
        except Product.DoesNotExist:
            # Remove invalid product from cart
            del cart[product_id]
            save_cart(request, cart)
    
    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
@transaction.atomic
def checkout(request):
    """Process checkout and create order."""
    cart = get_cart(request)
    
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('orders:cart')
    
    # Create order
    order = Order.objects.create(customer=request.user)
    total = Decimal('0.00')
    
    # Create order items
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_available=True)
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )
            
            total += quantity * price
        except Product.DoesNotExist:
            messages.warning(request, f'Product {product_id} is no longer available.')
    
    # Update order total
    order.total_price = total
    order.save()
    
    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True
    
    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def order_list(request):
    """List user's orders."""
    orders = Order.objects.filter(customer=request.user).prefetch_related('items')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail view."""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user owns the order or is admin
    if order.customer != request.user and not (hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('orders:order_list')
    
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
@user_passes_test(is_admin)
def admin_order_list(request):
    """Admin view of all orders."""
    orders = Order.objects.all().select_related('customer').prefetch_related('items')
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    return render(request, 'orders/admin_order_list.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    """Update order status (admin only)."""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('orders:admin_order_list')

