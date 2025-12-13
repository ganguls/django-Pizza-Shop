"""
Admin configuration for orders app.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem."""
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total']
    
    def get_total(self, obj):
        """Display total for order item."""
        if obj.pk:
            return obj.get_total()
        return '-'
    get_total.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ['id', 'customer', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__username', 'id']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'status', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""
    list_display = ['id', 'order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__id', 'product__name']
    
    def get_total(self, obj):
        """Display total for order item."""
        return obj.get_total()
    get_total.short_description = 'Total'

