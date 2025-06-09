from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import *


class ProductImageInline(StackedInline):
    model = ProductImage
    extra = 0
    tab = True
    fields = ['image', 'image_url', 'is_primary', 'alt_text']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'company', 'price', 'stock', 'is_available', 'is_featured', 'created_at')
    list_filter = ('category', 'company', 'is_available', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'company__name', 'category__name')


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email',)


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__email', 'product__name')


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'rating')
    search_fields = ('product__name', 'user__email')


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('user', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__email',)


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__user__email', 'product__name')


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('user', 'city', 'state')
    search_fields = ('user__email', 'address_line1', 'city', 'state')


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ('product', 'image', 'is_primary')
    list_filter = ('product', 'is_primary')