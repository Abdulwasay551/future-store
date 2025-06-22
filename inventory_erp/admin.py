from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Company, DeviceCategory, Device, DeviceIdentifier, Purchase, PurchaseItem, Sale, SaleItem, Dealer, Payment
from django.utils.html import format_html
from django.db.models import Sum, F
from django.urls import reverse
from django import forms
from .widgets import BarcodeInputWidget

# class DeviceIdentifierForm(forms.ModelForm):
#     class Meta:
#         model = DeviceIdentifier
#         fields = '__all__'
#         widgets = {
#             'identifier_value': BarcodeInputWidget(attrs={
#                 'class': 'barcode-input',
#                 'placeholder': 'Scan or enter IMEI/Serial number'
#             })
#         }

# class PurchaseItemInline(TabularInline):
#     model = PurchaseItem
#     extra = 0
#     fields = ['device', 'quantity', 'unit_price', 'received_quantity', 'total_price']
#     readonly_fields = ['total_price']

# class DeviceIdentifierInline(TabularInline):
#     model = DeviceIdentifier
#     form = DeviceIdentifierForm
#     extra = 0
#     fields = ['identifier_type', 'identifier_value', 'status', 'purchase_condition', 'notes']

# class SaleItemInline(TabularInline):
#     model = SaleItem
#     extra = 0
#     fields = ['device', 'device_identifier', 'quantity', 'unit_price', 'discount', 'total_price', 'warranty_months']
#     readonly_fields = ['total_price']

# class PaymentInline(TabularInline):
#     model = Payment
#     extra = 0
#     fields = ['payment_date', 'amount', 'payment_method', 'reference_number', 'notes']
#     readonly_fields = ['created_by']

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # Only set created_by on creation
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

# @admin.register(Dealer)
# class DealerAdmin(ModelAdmin):
#     list_display = ['name', 'dealer_type', 'contact_person', 'phone', 'credit_limit', 'outstanding_balance', 'is_active']
#     list_filter = ['dealer_type', 'is_active']
#     search_fields = ['name', 'contact_person', 'phone', 'email', 'cnic']
#     fieldsets = (
#         ('Basic Information', {
#             'fields': (('name', 'dealer_type'), ('contact_person', 'phone'), 'email', 'address', 'cnic')
#         }),
#         ('Financial Details', {
#             'fields': (('credit_limit', 'payment_terms_days'), 'is_active', 'notes')
#         }),
#     )

# @admin.register(Purchase)
# class PurchaseAdmin(ModelAdmin):
#     list_display = ['id', 'dealer', 'purchase_date', 'purchase_type', 'total_amount', 'paid_amount', 'balance_due', 'status'
# ]
#     list_filter = ['status', 'purchase_date', 'dealer', 'purchase_type']
#     search_fields = ['dealer__name', 'dealer_invoice_number', 'seller_cnic']
#     inlines = [PurchaseItemInline, DeviceIdentifierInline, PaymentInline]
#     fieldsets = (
#         ('Purchase Information', {
#             'fields': (('dealer', 'purchase_date'), ('dealer_invoice_number', 'purchase_type', 'seller_cnic'), 'status')
#         }),
#         ('Financial Details', {
#             'fields': (('total_amount', 'paid_amount'), 'payment_due_date', 'notes')
#         }),
#     )

# @admin.register(Sale)
# class SaleAdmin(ModelAdmin):
#     list_display = ['invoice_number', 'customer_name', 'sale_type', 'sale_date', 'final_amount', 'payment_status']
#     list_filter = ['sale_type', 'payment_status', 'status', 'sale_date']
#     search_fields = ['invoice_number', 'customer_name', 'customer_phone', 'customer_cnic']
#     inlines = [SaleItemInline, PaymentInline]
#     fieldsets = (
#         ('Customer Information', {
#             'fields': (('customer_name', 'customer_phone'), 'customer_email', 'customer_cnic', 'sale_type', 'sub_dealer')
#         }),
#         ('Sale Details', {
#             'fields': (('sale_date', 'invoice_number'), ('total_amount', 'discount', 'tax_amount', 'final_amount'),
#                       ('received_amount', 'payment_status', 'status'), 'notes')
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # Only set created_by on creation
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

# @admin.register(DeviceIdentifier)
# class DeviceIdentifierAdmin(ModelAdmin):
#     form = DeviceIdentifierForm
#     list_display = ['identifier_value', 'identifier_type', 'device', 'status', 'purchase_condition']
#     list_filter = ['identifier_type', 'status', 'purchase_condition']
#     search_fields = ['identifier_value', 'device__name', 'device__model_number']
#     raw_id_fields = ['device']

# @admin.register(Payment)
# class PaymentAdmin(ModelAdmin):
#     list_display = ['payment_type', 'payment_date', 'amount', 'payment_method', 'reference_number']
#     list_filter = ['payment_type', 'payment_method', 'payment_date']
#     search_fields = ['reference_number']
#     readonly_fields = ['created_by']

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # Only set created_by on creation
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

# @admin.register(Company)
# class CompanyAdmin(ModelAdmin):
#     list_display = ['name', 'contact_person', 'phone', 'is_active', 'created_at']
#     list_filter = ['is_active']
#     search_fields = ['name', 'contact_person', 'phone', 'email']
#     fieldsets = (
#         ('Company Information', {
#             'fields': (('name', 'is_active'), ('contact_person', 'phone'), 'email', 'website', 'logo')
#         }),
#         ('Additional Information', {
#             'fields': ('address', 'notes')
#         }),
#     )

# @admin.register(DeviceCategory)
# class DeviceCategoryAdmin(ModelAdmin):
#     list_display = ('name', 'created_at', 'updated_at')
#     search_fields = ('name',)
#     ordering = ('name',)


# @admin.register(Device)
# class DeviceAdmin(ModelAdmin):
#     list_display = ('name', 'sku', 'company', 'category', 'price', 'stock', 'stock_status')
#     list_filter = ('company', 'category', 'created_at')
#     search_fields = ('name', 'sku', 'company__name', 'category__name')
#     readonly_fields = ('sku', 'created_at', 'updated_at')
#     ordering = ('name',)
