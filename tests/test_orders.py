import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from decimal import Decimal
from products.models import Category, Product
from orders.models import Order, OrderItem
from accounts.models import UserProfile


@pytest.mark.django_db
class TestOrderModel:
    """Test Order model."""
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
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
            description='Test',
            price=Decimal('12.99'),
            category=category,
            is_available=True
        )
    
    def test_order_creation(self, user):
        """Test order creation."""
        order = Order.objects.create(
            customer=user,
            status='pending',
            total_price=Decimal('0.00')
        )
        assert order.customer == user
        assert order.status == 'pending'
        assert str(order) == f'Order #{order.id} - testuser - pending'
    
    def test_order_calculate_total(self, user, product):
        """Test order total calculation."""
        order = Order.objects.create(
            customer=user,
            status='pending'
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price=product.price
        )
        total = order.calculate_total()
        assert total == Decimal('25.98')
        assert order.total_price == Decimal('25.98')


@pytest.mark.django_db
class TestOrderItemModel:
    """Test OrderItem model."""
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='pass123')
    
    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Test', slug='test')
    
    @pytest.fixture
    def product(self, category):
        return Product.objects.create(
            name='Pizza',
            description='Test',
            price=Decimal('10.00'),
            category=category
        )
    
    @pytest.fixture
    def order(self, user):
        return Order.objects.create(customer=user)
    
    def test_order_item_creation(self, order, product):
        """Test order item creation."""
        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=3,
            price=product.price
        )
        assert item.quantity == 3
        assert item.price == Decimal('10.00')
        assert str(item) == f'3x Pizza - Order #{order.id}'
    
    def test_order_item_get_total(self, order, product):
        """Test order item total calculation."""
        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=5,
            price=Decimal('12.50')
        )
        assert item.get_total() == Decimal('62.50')


@pytest.mark.django_db
class TestCartViews:
    """Test cart views."""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
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
            description='Test',
            price=Decimal('12.99'),
            category=category,
            is_available=True
        )
    
    def test_cart_view_requires_login(self, client):
        """Test cart view requires authentication."""
        response = client.get(reverse('orders:cart'))
        assert response.status_code == 302  # Redirect to login
    
    def test_cart_view_empty(self, client, user):
        """Test empty cart view."""
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('orders:cart'))
        assert response.status_code == 200
    
    def test_add_to_cart(self, client, user, product):
        """Test adding product to cart."""
        client.login(username='testuser', password='testpass123')
        response = client.get(
            reverse('orders:add_to_cart', args=[product.pk]),
            {'quantity': '2'}
        )
        assert response.status_code == 302  # Redirect
        
        # Check cart in session
        session = client.session
        assert 'cart' in session
        assert str(product.pk) in session['cart']
        assert session['cart'][str(product.pk)]['quantity'] == 2
    
    def test_add_to_cart_requires_login(self, client, product):
        """Test add to cart requires authentication."""
        response = client.get(reverse('orders:add_to_cart', args=[product.pk]))
        assert response.status_code == 302  # Redirect to login
    
    def test_remove_from_cart(self, client, user, product):
        """Test removing product from cart."""
        client.login(username='testuser', password='testpass123')
        
        # Add to cart first
        session = client.session
        session['cart'] = {
            str(product.pk): {
                'quantity': 1,
                'price': str(product.price),
                'name': product.name
            }
        }
        session.save()
        
        response = client.post(reverse('orders:remove_from_cart', args=[product.pk]))
        assert response.status_code == 302
        
        # Check cart is empty
        session = client.session
        assert str(product.pk) not in session.get('cart', {})
    
    def test_update_cart(self, client, user, product):
        """Test updating cart quantity."""
        client.login(username='testuser', password='testpass123')
        
        # Add to cart first
        session = client.session
        session['cart'] = {
            str(product.pk): {
                'quantity': 1,
                'price': str(product.price),
                'name': product.name
            }
        }
        session.save()
        
        response = client.post(
            reverse('orders:update_cart', args=[product.pk]),
            {'quantity': '5'}
        )
        assert response.status_code == 302
        
        # Check quantity updated
        session = client.session
        assert session['cart'][str(product.pk)]['quantity'] == 5


@pytest.mark.django_db
class TestOrderViews:
    """Test order views."""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
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
            description='Test',
            price=Decimal('12.99'),
            category=category,
            is_available=True
        )
    
    def test_checkout_creates_order(self, client, user, product):
        """Test checkout creates order."""
        client.login(username='testuser', password='testpass123')
        
        # Add to cart
        session = client.session
        session['cart'] = {
            str(product.pk): {
                'quantity': 2,
                'price': str(product.price),
                'name': product.name
            }
        }
        session.save()
        
        response = client.post(reverse('orders:checkout'))
        assert response.status_code == 302  # Redirect after checkout
        
        # Check order created
        order = Order.objects.filter(customer=user).first()
        assert order is not None
        assert order.items.count() == 1
        assert order.total_price == Decimal('25.98')
        
        # Check cart is cleared
        session = client.session
        assert session.get('cart', {}) == {}
    
    def test_order_list_view(self, client, user):
        """Test order list view."""
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('orders:order_list'))
        assert response.status_code == 200
    
    def test_order_detail_view(self, client, user, product):
        """Test order detail view."""
        client.login(username='testuser', password='testpass123')
        
        order = Order.objects.create(customer=user)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )
        
        response = client.get(reverse('orders:order_detail', args=[order.id]))
        assert response.status_code == 200
        assert response.context['order'] == order


