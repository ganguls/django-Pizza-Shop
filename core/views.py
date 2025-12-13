"""
Views for core app - homepage and common views.
"""
from django.shortcuts import render
from products.models import Product, Category


def is_admin(user):
    """Check if user is an admin."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin()


def home_view(request):
    """Homepage view."""
    # Admins can see all products, customers only see available ones
    if is_admin(request.user):
        featured_products = Product.objects.all()[:6]
    else:
        featured_products = Product.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()[:4]
    
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'is_admin': is_admin(request.user),
    })

