from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, F, Q, Count
from django.core.exceptions import ValidationError
from .models import *
import json
from datetime import datetime
from decimal import Decimal
# import weasyprint  # For PDF generation - temporarily disabled
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

@staff_member_required
def erp_dashboard(request):
    # Get dealers with pending payments using F() expressions
    dealers_with_pending = Dealer.objects.annotate(
        total_pending=Sum(
            F('purchases__total_amount') - F('purchases__paid_amount'),
            filter=models.Q(purchases__status='pending')
        )
    ).filter(total_pending__gt=0)

    context = {
        'total_purchases': Purchase.objects.count(),
        'total_sales': Sale.objects.count(),
        'total_dealers': Dealer.objects.count(),
        'recent_purchases': Purchase.objects.order_by('-created_at')[:5],
        'recent_sales': Sale.objects.order_by('-created_at')[:5],
        'pending_payments': dealers_with_pending
    }
    return render(request, 'inventory_erp/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def device_list(request):
    companies = Company.objects.all()
    categories = DeviceCategory.objects.all()

    # Get filter parameters
    company_id = request.GET.get('company')
    category_id = request.GET.get('category')
    search = request.GET.get('search')

    # Start with all devices
    devices = Device.objects.all()

    # Apply filters
    if company_id:
        devices = devices.filter(company_id=company_id)
    if category_id:
        devices = devices.filter(category_id=category_id)
    if search:
        devices = devices.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search) |
            Q(company__name__icontains=search)
        )

    # Paginate results
    paginator = Paginator(devices, 10)
    page = request.GET.get('page')
    devices = paginator.get_page(page)

    context = {
        'devices': devices,
        'companies': companies,
        'categories': categories,
        'selected_company': company_id,
        'selected_category': category_id,
        'search': search,
    }
    return render(request, 'inventory_erp/device_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    # TODO: Implement transaction history
    transactions = []
    
    context = {
        'device': device,
        'transactions': transactions,
    }
    return render(request, 'inventory_erp/device_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_device(request):
    if request.method == 'POST':
        # TODO: Implement device form and form handling
        name = request.POST.get('name')
        company_id = request.POST.get('company')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            device = Device.objects.create(
                name=name,
                company_id=company_id,
                category_id=category_id,
                price=price,
                stock=stock,
                description=description,
                image=image
            )
            messages.success(request, 'Device added successfully!')
            return redirect('inventory_erp:device_detail', pk=device.pk)
        except Exception as e:
            messages.error(request, f'Error adding device: {str(e)}')
            return redirect('inventory_erp:add_device')

    companies = Company.objects.all()
    categories = DeviceCategory.objects.all()
    context = {
        'companies': companies,
        'categories': categories,
        'form_title': 'Add New Device',
        'submit_text': 'Add Device',
    }
    return render(request, 'inventory_erp/device_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_device(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        # TODO: Implement device form and form handling
        try:
            device.name = request.POST.get('name')
            device.company_id = request.POST.get('company')
            device.category_id = request.POST.get('category')
            device.price = request.POST.get('price')
            device.stock = request.POST.get('stock')
            device.description = request.POST.get('description')
            
            if 'image' in request.FILES:
                device.image = request.FILES['image']
            
            device.save()
            messages.success(request, 'Device updated successfully!')
            return redirect('inventory_erp:device_detail', pk=device.pk)
        except Exception as e:
            messages.error(request, f'Error updating device: {str(e)}')
            return redirect('inventory_erp:edit_device', pk=pk)

    companies = Company.objects.all()
    categories = DeviceCategory.objects.all()
    context = {
        'device': device,
        'companies': companies,
        'categories': categories,
        'form_title': 'Edit Device',
        'submit_text': 'Update Device',
    }
    return render(request, 'inventory_erp/device_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        try:
            device.delete()
            messages.success(request, 'Device deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting device: {str(e)}')
    return redirect('inventory_erp:device_list')

@staff_member_required
def purchase_entry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            dealer = Dealer.objects.get(id=data['dealer_id'])
            purchase = Purchase.objects.create(
                dealer=dealer,
                purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date(),
                dealer_invoice_number=data['invoice_number'],
                purchase_type=data['purchase_type'],
                total_amount=data['total_amount'],
                payment_due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None,
                status='pending'
            )
            
            # Create purchase items and device identifiers
            for item in data['items']:
                device = Device.objects.get(id=item['device_id'])
                purchase_item = PurchaseItem.objects.create(
                    purchase=purchase,
                    device=device,
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    received_quantity=item['quantity']
                )
                
                # Create device identifiers
                for identifier in item['identifiers']:
                    DeviceIdentifier.objects.create(
                        device=device,
                        identifier_type=identifier['type'],
                        identifier_value=identifier['value'],
                        purchase=purchase,
                        status='in_stock'
                    )
            
            # Create ledger entry if credit purchase
            if data['payment_type'] == 'credit':
                Ledger.objects.create(
                    dealer=dealer,
                    purchase=purchase,
                    transaction_date=purchase.purchase_date,
                    amount=purchase.total_amount,
                    payment_type='credit',
                    created_by=request.user
                )
            
            return JsonResponse({'status': 'success', 'purchase_id': purchase.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    dealers = Dealer.objects.filter(is_active=True)
    devices = Device.objects.filter(is_active=True).select_related('company')
    return render(request, 'inventory_erp/purchase_entry.html', {
        'dealers': dealers, 
        'devices': devices,
        'today': datetime.now().date(),
    })

@staff_member_required
def validate_identifier(request):
    identifier = request.GET.get('identifier')
    device_id = request.GET.get('device_id')
    
    existing = DeviceIdentifier.objects.filter(identifier_value=identifier).first()
    if existing:
        return JsonResponse({
            'valid': False,
            'message': f'This {existing.get_identifier_type_display()} is already registered'
        })
    return JsonResponse({'valid': True})

@staff_member_required
def print_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    html = render_to_string('inventory_erp/print/purchase.html', {'purchase': purchase})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=purchase_{purchase.id}.pdf'
    # weasyprint.HTML(string=html).write_pdf(response)
    return response

@staff_member_required
def dealer_ledger(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    ledger_entries = dealer.ledger_entries.all().order_by('transaction_date')
    return render(request, 'inventory_erp/dealer_ledger.html', {
        'dealer': dealer,
        'ledger_entries': ledger_entries
    })

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'inventory_erp/company_list.html'
    context_object_name = 'companies'
    
    def get_queryset(self):
        return Company.objects.all().order_by('-created_at')

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'inventory_erp/company_form.html'
    fields = ['name', 'contact_person', 'phone', 'email', 'address', 
              'website', 'logo', 'is_active', 'notes']
    success_url = reverse_lazy('inventory_erp:company_list')

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'inventory_erp/company_form.html'
    fields = ['name', 'contact_person', 'phone', 'email', 'address', 
              'website', 'logo', 'is_active', 'notes']
    success_url = reverse_lazy('inventory_erp:company_list')

class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'inventory_erp/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = self.object.devices.all()
        return context

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_list(request):
    # Get filter parameters
    dealer_type = request.GET.get('type')
    search = request.GET.get('search')
    is_active = request.GET.get('status', 'active')

    # Start with all dealers
    dealers = Dealer.objects.all()

    # Apply filters
    if dealer_type:
        dealers = dealers.filter(dealer_type=dealer_type)
    if search:
        dealers = dealers.filter(
            Q(name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )
    if is_active:
        dealers = dealers.filter(is_active=is_active == 'active')

    # Add aggregated data
    dealers = dealers.annotate(
        total_purchases=Sum('purchases__total_amount'),
        total_paid=Sum('purchases__paid_amount'),
        balance=F('total_purchases') - F('total_paid')
    )

    # Paginate results
    paginator = Paginator(dealers, 10)
    page = request.GET.get('page')
    dealers = paginator.get_page(page)

    context = {
        'dealers': dealers,
        'dealer_type': dealer_type,
        'search': search,
        'is_active': is_active,
        'dealer_types': Dealer.DEALER_TYPES,
    }
    return render(request, 'inventory_erp/dealer_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_create(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            dealer = Dealer.objects.create(
                name=data['name'],
                dealer_type=data['dealer_type'],
                contact_person=data['contact_person'],
                phone=data['phone'],
                email=data.get('email'),
                address=data['address'],
                cnic=data.get('cnic'),
                credit_limit=data.get('credit_limit'),
                payment_terms_days=data.get('payment_terms_days', 30),
                notes=data.get('notes', '')
            )
            messages.success(request, 'Dealer added successfully!')
            return redirect('inventory_erp:dealer_detail', pk=dealer.pk)
        except Exception as e:
            messages.error(request, f'Error adding dealer: {str(e)}')
            return redirect('inventory_erp:dealer_create')

    context = {
        'dealer_types': Dealer.DEALER_TYPES,
        'form_title': 'Add New Dealer',
        'submit_text': 'Add Dealer',
    }
    return render(request, 'inventory_erp/dealer_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_detail(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    
    # Get recent purchases
    recent_purchases = dealer.purchases.all().order_by('-purchase_date')[:5]
    
    # Get ledger entries
    ledger_entries = dealer.ledger_entries.all().order_by('-transaction_date')[:10]
    
    # Calculate summary
    summary = {
        'total_purchases': dealer.purchases.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_paid': dealer.purchases.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0,
        'outstanding_balance': dealer.outstanding_balance,
    }
    
    context = {
        'dealer': dealer,
        'recent_purchases': recent_purchases,
        'ledger_entries': ledger_entries,
        'summary': summary,
    }
    return render(request, 'inventory_erp/dealer_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_edit(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            dealer.name = data['name']
            dealer.dealer_type = data['dealer_type']
            dealer.contact_person = data['contact_person']
            dealer.phone = data['phone']
            dealer.email = data.get('email')
            dealer.address = data['address']
            dealer.cnic = data.get('cnic')
            dealer.credit_limit = data.get('credit_limit')
            dealer.payment_terms_days = data.get('payment_terms_days', 30)
            dealer.notes = data.get('notes', '')
            dealer.save()
            
            messages.success(request, 'Dealer updated successfully!')
            return redirect('inventory_erp:dealer_detail', pk=dealer.pk)
        except Exception as e:
            messages.error(request, f'Error updating dealer: {str(e)}')
            return redirect('inventory_erp:dealer_edit', pk=pk)

    context = {
        'dealer': dealer,
        'dealer_types': Dealer.DEALER_TYPES,
        'form_title': 'Edit Dealer',
        'submit_text': 'Update Dealer',
    }
    return render(request, 'inventory_erp/dealer_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_delete(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    if request.method == 'POST':
        try:
            dealer.is_active = False
            dealer.save()
            messages.success(request, 'Dealer deactivated successfully!')
        except Exception as e:
            messages.error(request, f'Error deactivating dealer: {str(e)}')
    return redirect('inventory_erp:dealer_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_ledger(request, dealer_id=None):
    dealer = None
    ledger_entries = []
    dealers = Dealer.objects.filter(is_active=True)
    
    if dealer_id:
        dealer = get_object_or_404(Dealer, pk=dealer_id)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Get ledger entries
        ledger_entries = dealer.ledger_entries.all()
        if start_date:
            ledger_entries = ledger_entries.filter(transaction_date__gte=start_date)
        if end_date:
            ledger_entries = ledger_entries.filter(transaction_date__lte=end_date)
            
        ledger_entries = ledger_entries.order_by('transaction_date')
        
        # Calculate running balance
        balance = 0
        for entry in ledger_entries:
            if entry.payment_type == 'credit':
                balance += entry.amount
            else:
                balance -= entry.amount
            entry.running_balance = balance
    
    context = {
        'dealer': dealer,
        'dealers': dealers,
        'ledger_entries': ledger_entries,
    }
    return render(request, 'inventory_erp/dealer_ledger.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def dealer_report(request):
    # Get filter parameters
    dealer_type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Start with all dealers
    dealers = Dealer.objects.filter(is_active=True)
    if dealer_type:
        dealers = dealers.filter(dealer_type=dealer_type)
        
    # Add aggregated data within date range
    purchase_filter = Q()
    if start_date:
        purchase_filter &= Q(purchases__purchase_date__gte=start_date)
    if end_date:
        purchase_filter &= Q(purchases__purchase_date__lte=end_date)
        
    dealers = dealers.annotate(
        total_purchases=Sum('purchases__total_amount', filter=purchase_filter),
        total_paid=Sum('purchases__paid_amount', filter=purchase_filter),
        balance=F('total_purchases') - F('total_paid')
    )
    
    context = {
        'dealers': dealers,
        'dealer_type': dealer_type,
        'start_date': start_date,
        'end_date': end_date,
        'dealer_types': Dealer.DEALER_TYPES,
        'total_outstanding': sum(d.balance or 0 for d in dealers),
    }
    return render(request, 'inventory_erp/dealer_report.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-purchase_date')
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        purchases = purchases.filter(purchase_date__range=[start_date, end_date])

    # Filter by dealer
    dealer_id = request.GET.get('dealer')
    if dealer_id:
        purchases = purchases.filter(dealer_id=dealer_id)

    # Filter by status
    status = request.GET.get('status')
    if status:
        purchases = purchases.filter(status=status)

    # Search
    search = request.GET.get('search')
    if search:
        purchases = purchases.filter(
            Q(dealer_invoice_number__icontains=search) |
            Q(dealer__name__icontains=search)
        )

    paginator = Paginator(purchases, 20)
    page = request.GET.get('page')
    purchases = paginator.get_page(page)

    context = {
        'purchases': purchases,
        'dealers': Dealer.objects.all(),
        'status_choices': Purchase.STATUS_CHOICES,
    }
    return render(request, 'inventory_erp/purchase_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def purchase_return_list(request):
    # Implement purchase return functionality
    context = {
        'message': 'Purchase Returns feature coming soon'
    }
    return render(request, 'inventory_erp/purchase_return_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def purchase_payments(request):
    payments = Payment.objects.filter(payment_type='purchase').order_by('-payment_date')
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        payments = payments.filter(payment_date__range=[start_date, end_date])

    # Filter by dealer through purchase
    dealer_id = request.GET.get('dealer')
    if dealer_id:
        payments = payments.filter(purchase__dealer_id=dealer_id)

    paginator = Paginator(payments, 20)
    page = request.GET.get('page')
    payments = paginator.get_page(page)

    context = {
        'payments': payments,
        'dealers': Dealer.objects.all(),
    }
    return render(request, 'inventory_erp/purchase_payments.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def sale_list(request):
    sales = Sale.objects.all().order_by('-sale_date')
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        sales = sales.filter(sale_date__range=[start_date, end_date])

    # Filter by sale type
    sale_type = request.GET.get('sale_type')
    if sale_type:
        sales = sales.filter(sale_type=sale_type)

    # Filter by status
    status = request.GET.get('status')
    if status:
        sales = sales.filter(status=status)

    # Search
    search = request.GET.get('search')
    if search:
        sales = sales.filter(
            Q(invoice_number__icontains=search) |
            Q(customer_name__icontains=search) |
            Q(customer_phone__icontains=search)
        )

    paginator = Paginator(sales, 20)
    page = request.GET.get('page')
    sales = paginator.get_page(page)

    context = {
        'sales': sales,
        'sale_types': Sale.SALE_TYPES,
        'status_choices': Sale.STATUS_CHOICES,
    }
    return render(request, 'inventory_erp/sale_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def sale_entry(request):
    if request.method == 'POST':
        # Process sale form data
        pass
    context = {
        'devices': Device.objects.filter(is_active=True),
        'dealers': Dealer.objects.filter(dealer_type='sub', is_active=True),
        'today': datetime.now().date(),
    }
    return render(request, 'inventory_erp/sale_entry.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def sale_return_list(request):
    # Implement sale return functionality
    context = {
        'message': 'Sale Returns feature coming soon'
    }
    return render(request, 'inventory_erp/sale_return_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def sale_payments(request):
    payments = Payment.objects.filter(payment_type='sale').order_by('-payment_date')
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        payments = payments.filter(payment_date__range=[start_date, end_date])

    paginator = Paginator(payments, 20)
    page = request.GET.get('page')
    payments = paginator.get_page(page)

    context = {
        'payments': payments,
    }
    return render(request, 'inventory_erp/sale_payments.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def sales_report(request):
    start_date = request.GET.get('start_date', timezone.now().date().replace(day=1))
    end_date = request.GET.get('end_date', timezone.now().date())

    sales = Sale.objects.filter(
        sale_date__range=[start_date, end_date]
    )

    summary = {
        'total_sales': sales.count(),
        'total_amount': sales.aggregate(total=Sum('final_amount'))['total'] or 0,
        'received_amount': sales.aggregate(total=Sum('received_amount'))['total'] or 0,
        'pending_amount': sales.aggregate(total=Sum('balance_due'))['total'] or 0,
    }

    # Daily sales chart data
    daily_sales = sales.values('sale_date').annotate(
        count=Count('id'),
        amount=Sum('final_amount')
    ).order_by('sale_date')

    context = {
        'summary': summary,
        'daily_sales': list(daily_sales),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'inventory_erp/sales_report.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def purchase_report(request):
    start_date = request.GET.get('start_date', timezone.now().date().replace(day=1))
    end_date = request.GET.get('end_date', timezone.now().date())

    purchases = Purchase.objects.filter(
        purchase_date__range=[start_date, end_date]
    )

    summary = {
        'total_purchases': purchases.count(),
        'total_amount': purchases.aggregate(total=Sum('total_amount'))['total'] or 0,
        'paid_amount': purchases.aggregate(total=Sum('paid_amount'))['total'] or 0,
        'pending_amount': purchases.aggregate(total=Sum('balance_due'))['total'] or 0,
    }

    # Dealer-wise summary
    dealer_summary = purchases.values('dealer__name').annotate(
        count=Count('id'),
        total=Sum('total_amount'),
        paid=Sum('paid_amount')
    ).order_by('-total')

    context = {
        'summary': summary,
        'dealer_summary': dealer_summary,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'inventory_erp/purchase_report.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def inventory_report(request):
    # Get all active devices with their stock levels
    devices = Device.objects.filter(is_active=True)

    summary = {
        'total_devices': devices.count(),
        'low_stock': devices.filter(stock__gt=0, stock__lte=10).count(),
        'out_of_stock': devices.filter(stock=0).count(),
         'total_stock_value': sum(device.stock * (device.price or 0) for device in devices),
    }

    # Category-wise summary using annotate
    category_summary = devices.values('category__name').annotate(
        count=Count('id'),
        total_stock=Sum('stock'),
        stock_value=Sum(F('stock') * F('price'))
    ).order_by('-count')

    context = {
        'summary': summary,
        'category_summary': category_summary,
        'devices': devices,
    }
    return render(request, 'inventory_erp/inventory_report.html', context)

def generate_pdf_report(request):
    # Temporary response while PDF generation is disabled
    return HttpResponse("PDF generation is temporarily disabled. Please check back later.", content_type="text/plain")
    
    # Original PDF generation code - temporarily commented out
    # context = {
    #     'products': Product.objects.all(),
    #     'date': timezone.now()
    # }
    # html = render_to_string('inventory_erp/pdf_report.html', context)
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
    # weasyprint.HTML(string=html).write_pdf(response)
    # return response
