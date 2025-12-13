"""
Views for products app - product listing and management.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Category


def is_admin(user):
    """Check if user is an admin."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin()


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin role."""
    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('core:home')


class ProductListView(ListView):
    """List all available products (or all products for admins)."""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        # Admins can see all products, customers only see available ones
        if is_admin(self.request.user):
            queryset = Product.objects.all().select_related('category')
        else:
            queryset = Product.objects.filter(is_available=True).select_related('category')
        
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['is_admin'] = is_admin(self.request.user)
        return context


class ProductDetailView(DetailView):
    """Product detail view."""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Create new product (admin only)."""
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image', 'category', 'is_available']
    success_url = reverse_lazy('products:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Update product (admin only)."""
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image', 'category', 'is_available']
    success_url = reverse_lazy('products:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Delete product (admin only)."""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)


def category_detail(request, slug):
    """Category detail view with products."""
    category = get_object_or_404(Category, slug=slug)
    # Admins can see all products, customers only see available ones
    if is_admin(request.user):
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(category=category, is_available=True)
    return render(request, 'products/category_detail.html', {
        'category': category,
        'products': products,
        'is_admin': is_admin(request.user)
    })

