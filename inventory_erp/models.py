from django.db import models
from django.core.validators import MinValueValidator
from user_auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

class Company(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='inventory/companies/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

class DeviceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Device Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Device(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, editable=False,default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='devices')
    category = models.ForeignKey(DeviceCategory, on_delete=models.CASCADE, related_name='devices',null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    discount_type = models.CharField(max_length=10, choices=[
        ('none', 'No Discount'),
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage')
    ], default='none')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                     help_text="Fixed amount or percentage value")
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='devices/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate SKU: First 3 letters of company name + UUID4 first 8 chars
            company_prefix = self.company.name[:3].upper()
            unique_id = str(uuid.uuid4())[:8]
            self.sku = f"{company_prefix}-{unique_id}"
        super().save(*args, **kwargs)

    @property
    def stock_status(self):
        if self.stock > 10:
            return 'In Stock'
        elif self.stock > 0:
            return 'Low Stock'
        return 'Out of Stock'
        
    @property
    def discounted_price(self):
        if not self.price:
            return None
        if self.discount_type == 'none' or not self.discount_value:
            return self.price
        if self.discount_type == 'fixed':
            return max(0, self.price - self.discount_value)
        if self.discount_type == 'percentage':
            discount_amount = (self.price * self.discount_value) / 100
            return max(0, self.price - discount_amount)

    @property
    def discount_amount(self):
        if not self.price or self.discount_type == 'none' or not self.discount_value:
            return 0
        if self.discount_type == 'fixed':
            return min(self.price, self.discount_value)
        if self.discount_type == 'percentage':
            return (self.price * self.discount_value) / 100

class Dealer(models.Model):
    DEALER_TYPES = (
        ('main', 'Main Dealer'),
        ('sub', 'Sub Dealer'),
        ('second_hand', 'Second Hand Dealer'),
    )
    name = models.CharField(max_length=200)
    dealer_type = models.CharField(max_length=15, choices=DEALER_TYPES)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    cnic = models.CharField(max_length=15, blank=True, null=True, 
                          help_text="Required for second-hand dealers")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, 
                                     null=True, blank=True,
                                     help_text="Credit limit for main/sub dealers")
    payment_terms_days = models.PositiveIntegerField(default=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_dealer_type_display()})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.dealer_type == 'second_hand' and not self.cnic:
            raise ValidationError({'cnic': 'CNIC is required for second-hand dealers'})
        if self.dealer_type in ['main', 'sub'] and not self.credit_limit:
            raise ValidationError({'credit_limit': 'Credit limit is required for main/sub dealers'})

    @property
    def outstanding_balance(self):
        return sum(p.balance_due for p in self.purchases.all())

class Purchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    )
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT, related_name='purchases')
    purchase_date = models.DateField()
    dealer_invoice_number = models.CharField(max_length=50, help_text="Invoice number from dealer")
    purchase_type = models.CharField(max_length=15, choices=[
        ('new', 'New Stock'),
        ('second_hand', 'Second Hand')
    ])
    seller_cnic = models.CharField(max_length=15, blank=True, null=True,
                                 help_text="Required for second-hand purchases")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO-{self.id} - {self.dealer.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.purchase_type == 'second_hand' and not self.seller_cnic:
            raise ValidationError({'seller_cnic': 'CNIC is required for second-hand purchases'})

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount

class DeviceIdentifier(models.Model):
    IDENTIFIER_TYPES = (
        ('imei', 'IMEI Number'),
        ('serial', 'Serial Number'),
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='identifiers',null=True, blank=True)
    identifier_type = models.CharField(max_length=6, choices=IDENTIFIER_TYPES)
    identifier_value = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, default='in_stock', 
                            choices=[('in_stock', 'In Stock'), 
                                   ('reserved', 'Reserved'),
                                   ('sold', 'Sold')])
    purchase = models.ForeignKey('Purchase', on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='devices')
    sale = models.ForeignKey('Sale', on_delete=models.SET_NULL, 
                            null=True, blank=True, related_name='devices')
    purchase_condition = models.CharField(max_length=20, 
                                       choices=[('new', 'New'),
                                              ('used', 'Used'),
                                              ('refurbished', 'Refurbished')],
                                       default='new')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.identifier_type.upper()}: {self.identifier_value}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE, related_name='items')
    device = models.ForeignKey(Device, on_delete=models.PROTECT,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    received_quantity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    @property
    def total_price(self):
        if self.quantity is None or self.unit_price is None:
            return 0
        return self.quantity * self.unit_price

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.received_quantity > self.quantity:
            raise ValidationError({
                'received_quantity': 'Received quantity cannot be greater than ordered quantity'
            })

class Sale(models.Model):
    SALE_TYPES = (
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    customer_cnic = models.CharField(max_length=15, blank=True, null=True)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPES)
    sub_dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT, 
                                 null=True, blank=True,
                                 limit_choices_to={'dealer_type': 'sub'})
    sale_date = models.DateField()
    invoice_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    received_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, 
                                   choices=[('paid', 'Paid'),
                                          ('partial', 'Partial'),
                                          ('pending', 'Pending')])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"INV-{self.invoice_number}"

    @property
    def balance_due(self):
        return self.final_amount - self.received_amount

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.sale_type == 'wholesale' and not self.sub_dealer:
            raise ValidationError({'sub_dealer': 'Sub-dealer is required for wholesale sales'})

class SaleItem(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='items')
    device = models.ForeignKey(Device, on_delete=models.PROTECT, null=True, blank=True)
    device_identifier = models.ForeignKey(DeviceIdentifier, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    warranty_months = models.PositiveIntegerField(default=12)
    notes = models.TextField(blank=True)

class Payment(models.Model):
    PAYMENT_TYPES = (
        ('purchase', 'Purchase Payment'),
        ('sale', 'Sale Payment'),
    )
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    )
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=50, blank=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name='payments')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, 
                           null=True, blank=True, related_name='payments')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Ledger(models.Model):
    dealer = models.ForeignKey('Dealer', on_delete=models.PROTECT, related_name='ledger_entries')
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE, null=True, blank=True)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=[
        ('credit', 'Credit'),
        ('net', 'Net Payment')
    ])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.dealer.name} - {self.amount} ({self.get_payment_type_display()})"
