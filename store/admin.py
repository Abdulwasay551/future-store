from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import *
import json


class ProductImageInline(StackedInline):
    model = ProductImage
    extra = 0
    tab = True
    fields = ['image', 'image_url', 'is_primary', 'alt_text', 'color']


class ProductColorInline(StackedInline):
    model = ProductColor
    extra = 0
    tab = True
    fields = ['name', 'hex_code', 'is_primary', 'stock']


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'image_url')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    fields = ['name', 'slug', 'description', 'image', 'image_url']


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'created_at', 'logo_url')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')
    fields = ['category', 'name', 'slug', 'logo', 'logo_url', 'description', 'is_featured']


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [ProductColorInline, ProductImageInline]
    list_display = ('name', 'category', 'company', 'price', 'total_stock', 'is_available', 'is_featured', 'created_at')
    list_filter = ('category', 'company', 'is_available', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'company__name', 'category__name')
    readonly_fields = ('total_stock', 'is_in_stock', 'formatted_features', 'formatted_specs')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'company')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'discount_type', 'discount_value', 'is_available')
        }),
        ('Product Details', {
            'fields': ('is_featured', 'release_date', 'specs', 'features')
        }),
        ('Stock Information', {
            'fields': ('total_stock', 'is_in_stock'),
            'classes': ('collapse',)
        }),
        ('Formatted Display', {
            'fields': ('formatted_features', 'formatted_specs'),
            'classes': ('collapse',),
            'description': 'Read-only formatted display of features and specs'
        }),
    )

    def formatted_features(self, obj):
        if obj.features:
            try:
                if isinstance(obj.features, str):
                    features = json.loads(obj.features)
                else:
                    features = obj.features
                
                if features.get('device'):
                    html = f"<h3>{features['device']}</h3>"
                else:
                    html = "<h3>Features</h3>"
                
                if features.get('features'):
                    html += "<ul>"
                    for feature in features['features']:
                        html += f"<li>{feature}</li>"
                    html += "</ul>"
                else:
                    html += "<ul>"
                    for key, value in features.items():
                        html += f"<li><strong>{key}:</strong> {value}</li>"
                    html += "</ul>"
                
                return html
            except:
                return "Error formatting features"
        return "No features"
    formatted_features.allow_tags = True
    formatted_features.short_description = "Formatted Features"

    def formatted_specs(self, obj):
        if obj.specs:
            try:
                if isinstance(obj.specs, str):
                    specs = json.loads(obj.specs)
                else:
                    specs = obj.specs
                
                if specs.get('device'):
                    html = f"<h3>{specs['device']}</h3>"
                else:
                    html = "<h3>Specifications</h3>"
                
                if specs.get('specifications'):
                    for category, category_specs in specs['specifications'].items():
                        html += f"<h4>{category.replace('_', ' ').title()}</h4>"
                        html += "<ul>"
                        for key, value in category_specs.items():
                            html += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"
                        html += "</ul>"
                else:
                    html += "<ul>"
                    for key, value in specs.items():
                        html += f"<li><strong>{key}:</strong> {value}</li>"
                    html += "</ul>"
                
                return html
            except:
                return "Error formatting specifications"
        return "No specifications"
    formatted_specs.allow_tags = True
    formatted_specs.short_description = "Formatted Specifications"


@admin.register(ProductColor)
class ProductColorAdmin(ModelAdmin):
    list_display = ('product', 'name', 'hex_code', 'is_primary', 'stock')
    list_filter = ('product', 'is_primary')
    search_fields = ('product__name', 'name')
    fields = ['product', 'name', 'hex_code', 'is_primary', 'stock']


@admin.register(DeliveryService)
class DeliveryServiceAdmin(ModelAdmin):
    list_display = ('name', 'estimated_delivery_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    fields = ['name', 'tracking_url_template', 'estimated_delivery_days', 'is_active']


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status_display', 'total_amount', 'payment_status', 'delivery_service', 'tracking_id', 'created_at')
    list_filter = ('status', 'payment_status', 'delivery_service', 'created_at')
    search_fields = ('user__email', 'tracking_id', 'id')
    readonly_fields = ('get_total', 'tracking_url')
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'address', 'status', 'total_amount', 'notes')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Tracking Information', {
            'fields': ('delivery_service', 'tracking_id', 'tracking_url', 'shipped_date', 'estimated_delivery_date', 'actual_delivery_date')
        }),
        ('Order Summary', {
            'fields': ('get_total',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        for order in queryset:
            order.update_status('confirmed')
        self.message_user(request, f"{queryset.count()} orders marked as confirmed.")
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"
    
    def mark_as_processing(self, request, queryset):
        for order in queryset:
            order.update_status('processing')
        self.message_user(request, f"{queryset.count()} orders marked as processing.")
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        for order in queryset:
            order.update_status('shipped')
        self.message_user(request, f"{queryset.count()} orders marked as shipped.")
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        for order in queryset:
            order.update_status('delivered')
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        for order in queryset:
            order.update_status('cancelled')
        self.message_user(request, f"{queryset.count()} orders marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'is_email_sent', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_email_sent', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fields = ['user', 'notification_type', 'title', 'message', 'order', 'is_read', 'is_email_sent']
    actions = ['mark_as_read', 'mark_as_unread', 'resend_email']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} notifications marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} notifications marked as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"
    
    def resend_email(self, request, queryset):
        sent_count = 0
        for notification in queryset:
            if notification.send_email_notification():
                sent_count += 1
        self.message_user(request, f"{sent_count} emails sent successfully.")
    resend_email.short_description = "Resend email notifications"


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email',)


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('cart', 'product', 'color', 'quantity')
    list_filter = ('cart', 'product', 'color')
    search_fields = ('cart__user__email', 'product__name', 'color__name')


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'rating')
    search_fields = ('product__name', 'user__email')


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
    list_display = ('product', 'color', 'is_primary', 'created_at', 'image_url')
    list_filter = ('product', 'color', 'is_primary')
    search_fields = ('product__name', 'color__name', 'alt_text')
    fields = ['product', 'color', 'image', 'image_url', 'is_primary', 'alt_text']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)