import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from products.models import Category, Product
from accounts.models import UserProfile


@pytest.mark.django_db
class TestCategoryModel:
    """Test Category model."""
    
    def test_category_creation(self):
        """Test category creation."""
        category = Category.objects.create(
            name='Classic Pizzas',
            slug='classic-pizzas',
            description='Traditional pizzas'
        )
        assert category.name == 'Classic Pizzas'
        assert category.slug == 'classic-pizzas'
        assert str(category) == 'Classic Pizzas'
    
    def test_category_get_absolute_url(self):
        """Test category absolute URL."""
        category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        url = category.get_absolute_url()
        assert 'test-category' in url


@pytest.mark.django_db
class TestProductModel:
    """Test Product model."""
    
    @pytest.fixture
    def category(self):
        return Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
    
    def test_product_creation(self, category):
        """Test product creation."""
        product = Product.objects.create(
            name='Margherita',
            description='Classic pizza',
            price=12.99,
            category=category,
            is_available=True
        )
        assert product.name == 'Margherita'
        assert product.price == 12.99
        assert product.is_available is True
        assert str(product) == 'Margherita'
    
    def test_product_get_absolute_url(self, category):
        """Test product absolute URL."""
        product = Product.objects.create(
            name='Test Pizza',
            description='Test',
            price=10.00,
            category=category
        )
        url = product.get_absolute_url()
        assert str(product.pk) in url


@pytest.mark.django_db
class TestProductViews:
    """Test product views."""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    @pytest.fixture
    def category(self):
        return Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
    
    @pytest.fixture
    def product(self, category):
        return Product.objects.create(
            name='Test Pizza',
            description='Test description',
            price=12.99,
            category=category,
            is_available=True
        )
    
    @pytest.fixture
    def customer_user(self):
        user = User.objects.create_user(
            username='customer',
            password='pass123'
        )
        return user
    
    @pytest.fixture
    def admin_user(self):
        user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        user.profile.role = 'admin'
        user.profile.save()
        return user
    
    def test_product_list_view(self, client, product):
        """Test product list view."""
        response = client.get(reverse('products:product_list'), follow=True)
        assert response.status_code == 200
        assert product in response.context['products']
    
    def test_product_list_view_filters_unavailable(self, client, category):
        """Test that unavailable products are hidden from customers."""
        available = Product.objects.create(
            name='Available',
            description='Test',
            price=10.00,
            category=category,
            is_available=True
        )
        unavailable = Product.objects.create(
            name='Unavailable',
            description='Test',
            price=10.00,
            category=category,
            is_available=False
        )
        response = client.get(reverse('products:product_list'), follow=True)
        assert response.status_code == 200
        products = list(response.context['products'])
        assert available in products
        assert unavailable not in products
    
    def test_product_list_view_shows_all_for_admin(self, client, category, admin_user):
        """Test that admins see all products."""
        available = Product.objects.create(
            name='Available',
            description='Test',
            price=10.00,
            category=category,
            is_available=True
        )
        unavailable = Product.objects.create(
            name='Unavailable',
            description='Test',
            price=10.00,
            category=category,
            is_available=False
        )
        client.login(username='admin', password='admin123')
        response = client.get(reverse('products:product_list'), follow=True)
        assert response.status_code == 200
        products = list(response.context['products'])
        assert available in products
        assert unavailable in products
    
    def test_product_detail_view(self, client, product):
        """Test product detail view."""
        response = client.get(reverse('products:product_detail', args=[product.pk]), follow=True)
        assert response.status_code == 200
        assert response.context['product'] == product
    
    def test_product_create_view_requires_admin(self, client, customer_user, category):
        """Test that only admins can create products."""
        client.login(username='customer', password='pass123')
        response = client.get(reverse('products:product_create'), follow=True)
        # Should redirect (non-admin access denied)
        assert response.status_code == 200
        assert len(response.redirect_chain) > 0
    
    def test_product_create_view_admin(self, client, admin_user, category):
        """Test admin can create products."""
        client.login(username='admin', password='admin123')
        response = client.get(reverse('products:product_create'), follow=True)
        assert response.status_code == 200
    
    def test_product_create_post(self, client, admin_user, category):
        """Test product creation via POST."""
        client.login(username='admin', password='admin123')
        response = client.post(reverse('products:product_create'), {
            'name': 'New Pizza',
            'description': 'New description',
            'price': '15.99',
            'category': category.pk,
            'is_available': True,
        }, follow=True)
        assert response.status_code == 200  # After following redirect
        assert Product.objects.filter(name='New Pizza').exists()
    
    def test_category_detail_view(self, client, category, product):
        """Test category detail view."""
        response = client.get(reverse('products:category_detail', args=[category.slug]), follow=True)
        assert response.status_code == 200
        assert category == response.context['category']
        assert product in response.context['products']


