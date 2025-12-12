from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('unit_price',)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'price', 'available')
    search_fields = ('name', 'sku')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_email', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]