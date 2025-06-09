from django.urls import path
from . import views

app_name = 'inventory_erp'

urlpatterns = [
    path('', views.erp_dashboard, name='dashboard'),
    path('devices/', views.device_list, name='device_list'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    path('devices/<int:pk>/edit/', views.edit_device, name='edit_device'),
    path('devices/<int:pk>/delete/', views.delete_device, name='delete_device'),
    path('purchase/entry/', views.purchase_entry, name='purchase_entry'),
    path('purchase/print/<int:pk>/', views.print_purchase, name='print_purchase'),
    path('dealer/ledger/<int:dealer_id>/', views.dealer_ledger, name='dealer_ledger'),
    path('api/validate-identifier/', views.validate_identifier, name='validate_identifier'),
    path('companies/', views.CompanyListView.as_view(), name='company_list'),
    path('companies/add/', views.CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('companies/<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_update'),

    # Dealer Management
    path('dealers/', views.dealer_list, name='dealer_list'),
    path('dealers/add/', views.dealer_create, name='dealer_create'),
    path('dealers/<int:pk>/', views.dealer_detail, name='dealer_detail'),
    path('dealers/<int:pk>/edit/', views.dealer_edit, name='dealer_edit'),
    path('dealers/<int:pk>/delete/', views.dealer_delete, name='dealer_delete'),
    path('dealers/ledger/', views.dealer_ledger, name='dealer_ledger'),
    path('dealers/report/', views.dealer_report, name='dealer_report'),

    # Purchase Management
    path('purchase/list/', views.purchase_list, name='purchase_list'),
    path('purchase/returns/', views.purchase_return_list, name='purchase_return_list'),
    path('purchase/payments/', views.purchase_payments, name='purchase_payments'),

    # Sales Management
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/new/', views.sale_entry, name='sale_entry'),
    path('sales/returns/', views.sale_return_list, name='sale_return_list'),
    path('sales/payments/', views.sale_payments, name='sale_payments'),

    # Reports
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/purchases/', views.purchase_report, name='purchase_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
]
