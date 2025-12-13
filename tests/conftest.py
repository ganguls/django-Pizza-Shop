"""
Pytest configuration and shared fixtures.
"""
import pytest
from django.contrib.auth.models import User
from products.models import Category, Product
from accounts.models import UserProfile


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name='Test Category',
        slug='test-category',
        description='Test category description'
    )


@pytest.fixture
def product(db, category):
    """Create a test product."""
    return Product.objects.create(
        name='Test Pizza',
        description='Test pizza description',
        price=12.99,
        category=category,
        is_available=True
    )


@pytest.fixture
def customer_user(db):
    """Create a customer user."""
    user = User.objects.create_user(
        username='customer',
        password='testpass123'
    )
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User.objects.create_user(
        username='admin',
        password='admin123'
    )
    user.profile.role = 'admin'
    user.profile.save()
    return user

