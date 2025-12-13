import pytest
from django.urls import reverse
from django.test import Client
from products.models import Category, Product
from accounts.models import UserProfile
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestHomeView:
    """Test home view."""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    @pytest.fixture
    def category(self):
        return Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test description'
        )
    
    @pytest.fixture
    def products(self, category):
        products = []
        for i in range(10):
            products.append(Product.objects.create(
                name=f'Pizza {i}',
                description='Test',
                price=10.00 + i,
                category=category,
                is_available=True
            ))
        return products
    
    def test_home_view(self, client):
        """Test home page loads."""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
    
    def test_home_view_shows_featured_products(self, client, products):
        """Test home page shows featured products."""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
        assert 'featured_products' in response.context
        assert len(response.context['featured_products']) <= 6
    
    def test_home_view_shows_categories(self, client, category):
        """Test home page shows categories."""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
        assert 'categories' in response.context

