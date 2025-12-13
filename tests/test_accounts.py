import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from accounts.models import UserProfile


@pytest.mark.django_db
class TestUserProfile:
    """Test UserProfile model."""
    
    def test_user_profile_created_on_user_creation(self):
        """Test that UserProfile is automatically created when User is created."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        assert hasattr(user, 'profile')
        assert user.profile.role == 'customer'
        assert user.profile.is_customer() is True
        assert user.profile.is_admin() is False
    
    def test_user_profile_str(self):
        """Test UserProfile string representation."""
        user = User.objects.create_user(username='testuser', password='testpass123')
        assert str(user.profile) == 'testuser - customer'
    
    def test_user_profile_is_admin(self):
        """Test is_admin method."""
        user = User.objects.create_user(username='admin', password='admin123')
        user.profile.role = 'admin'
        user.profile.save()
        assert user.profile.is_admin() is True
        assert user.profile.is_customer() is False
    
    def test_user_profile_is_customer(self):
        """Test is_customer method."""
        user = User.objects.create_user(username='customer', password='pass123')
        assert user.profile.is_customer() is True
        assert user.profile.is_admin() is False


@pytest.mark.django_db
class TestAuthenticationViews:
    """Test authentication views."""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    def test_register_view_get(self, client):
        """Test registration page loads."""
        response = client.get(reverse('accounts:register'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_register_view_post_success(self, client):
        """Test successful user registration."""
        response = client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        assert response.status_code == 302  # Redirect after success
        assert User.objects.filter(username='newuser').exists()
        user = User.objects.get(username='newuser')
        assert hasattr(user, 'profile')
    
    def test_register_view_post_invalid(self, client):
        """Test registration with invalid data."""
        response = client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'pass',
            'password2': 'different',
        })
        assert response.status_code == 200  # Stays on page
        assert not User.objects.filter(username='newuser').exists()
    
    def test_login_view_get(self, client):
        """Test login page loads."""
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200
    
    def test_login_view_post_success(self, client):
        """Test successful login."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        assert response.status_code == 302  # Redirect after login
    
    def test_login_view_post_invalid(self, client):
        """Test login with invalid credentials."""
        response = client.post(reverse('accounts:login'), {
            'username': 'nonexistent',
            'password': 'wrongpass',
        })
        assert response.status_code == 200  # Stays on page
    
    def test_logout_view(self, client):
        """Test logout."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('accounts:logout'))
        assert response.status_code == 302  # Redirect after logout
    
    def test_profile_view_requires_login(self, client):
        """Test profile view requires authentication."""
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 302  # Redirect to login
    
    def test_profile_view_authenticated(self, client):
        """Test profile view for authenticated user."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 200
        assert 'profile' in response.context

