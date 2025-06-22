from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user_auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import os

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Company(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='companies/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f"{self.name} - {self.category.name}"

class ProductColor(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50)  # e.g., "Red", "Blue", "Black"
    hex_code = models.CharField(max_length=7, blank=True)  # e.g., "#FF0000"
    is_primary = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other colors of this product to non-primary
            ProductColor.objects.filter(product=self.product).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        """Get the primary image for this color"""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.get_image_url
        # Fallback to first image if no primary is set
        first_image = self.images.first()
        if first_image:
            return first_image.get_image_url
        return None

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        color_name = f" ({self.color.name})" if self.color else ""
        return f"Image for {self.product.name}{color_name}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other images of this product/color to non-primary
            if self.color:
                ProductImage.objects.filter(product=self.product, color=self.color).exclude(id=self.id).update(is_primary=False)
            else:
                ProductImage.objects.filter(product=self.product, color__isnull=True).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=10, choices=[('none', 'None'), ('percentage', 'Percentage'), ('fixed', 'Fixed')], default='none')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    release_date = models.DateField(null=True, blank=True)
    specs = models.JSONField(default=dict, blank=True)  # For storing product specifications
    features = models.JSONField(default=dict, blank=True)  # For storing product features in tabular form
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.get_image_url
        # Fallback to first image if no primary is set
        first_image = self.images.first()
        if first_image:
            return first_image.get_image_url
        return None

    @property
    def discounted_price(self):
        if self.discount_type == 'none':
            return self.price
        elif self.discount_type == 'percentage':
            return round(self.price - (self.price * self.discount_value / 100), 2)
        elif self.discount_type == 'fixed':
            return round(max(self.price - self.discount_value, 0), 2)
        return self.price

    @property
    def has_discount(self):
        return self.discount_type != 'none' and self.discount_value > 0

    @property
    def primary_color(self):
        return self.colors.filter(is_primary=True).first()

    @property
    def total_stock(self):
        """Calculate total stock from all colors"""
        return sum(color.stock for color in self.colors.all())

    @property
    def is_in_stock(self):
        """Check if any color has stock"""
        return self.colors.filter(stock__gt=0).exists()

    @property
    def available_colors(self):
        """Get colors that have stock"""
        return self.colors.filter(stock__gt=0)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product', 'color')
    
    @property
    def subtotal(self):
        if self.quantity is None:
            return 0
        return self.product.discounted_price * self.quantity

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')  # One review per user per product

    def __str__(self):
        return f'{self.user.email} - {self.product.name} - {self.rating}'

class Address(models.Model):
    ADDRESS_TYPES = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES)
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.user.email} - {self.address_type} - {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other addresses of this user to non-default
            Address.objects.filter(user=self.user).exclude(id=self.id).update(is_default=False)
        elif not Address.objects.filter(user=self.user, is_default=True).exists():
            # If no default address exists for this user, make this one default
            self.is_default = True
        super().save(*args, **kwargs)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('order_created', 'Order Created'),
        ('order_status_updated', 'Order Status Updated'),
        ('order_shipped', 'Order Shipped'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('payment_received', 'Payment Received'),
        ('stock_low', 'Low Stock Alert'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.notification_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def send_email_notification(self):
        """Send email notification to user"""
        try:
            subject = self.title
            html_message = render_to_string('store/email/notification_email.html', {
                'notification': self,
                'user': self.user,
                'order': self.order,
            })
            plain_message = self.message
            
            print(f"Sending user email to: {self.user.email}")
            # Send to user
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"✅ User email sent successfully to {self.user.email}")
            
            # Send admin notification for order events
            if self.order and self.notification_type in ['order_created', 'order_status_updated']:
                admin_email = os.getenv('ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                print(f"Sending admin email to: {admin_email}")
                admin_subject = f"Order Update - {self.order.id}"
                admin_html_message = render_to_string('store/email/admin_notification_email.html', {
                    'notification': self,
                    'order': self.order,
                    'user': self.user,
                })
                
                send_mail(
                    subject=admin_subject,
                    message=f"Order {self.order.id} has been {self.get_notification_type_display()}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    html_message=admin_html_message,
                    fail_silently=False,
                )
                print(f"✅ Admin email sent successfully to {admin_email}")
            
            self.is_email_sent = True
            self.save()
            return True
        except Exception as e:
            print(f"❌ Failed to send email notification: {e}")
            import traceback
            traceback.print_exc()
            return False

class DeliveryService(models.Model):
    name = models.CharField(max_length=100)  # e.g., "FedEx", "DHL", "UPS"
    tracking_url_template = models.URLField(help_text="Template URL with {tracking_id} placeholder")
    estimated_delivery_days = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_tracking_url(self, tracking_id):
        """Generate tracking URL for a given tracking ID"""
        return self.tracking_url_template.format(tracking_id=tracking_id)

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Tracking Information
    delivery_service = models.ForeignKey(DeliveryService, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Order Details
    notes = models.TextField(blank=True, help_text="Special instructions or notes")
    payment_method = models.CharField(max_length=50, choices=[
        ('pending', 'Pending - Will be discussed with representative'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Transfer'),
        ('online_payment', 'Online Payment'),
    ], default='pending')
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

    @property
    def get_total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def tracking_url(self):
        """Get tracking URL if delivery service and tracking ID are available"""
        if self.delivery_service and self.tracking_id:
            return self.delivery_service.get_tracking_url(self.tracking_id)
        return None

    @property
    def status_display(self):
        """Get human-readable status with icons"""
        status_icons = {
            'pending': '⏳',
            'confirmed': '✅',
            'processing': '🔧',
            'shipped': '📦',
            'out_for_delivery': '🚚',
            'delivered': '🎉',
            'cancelled': '❌',
            'returned': '↩️',
        }
        return f"{status_icons.get(self.status, '📋')} {self.get_status_display()}"

    def update_status(self, new_status, tracking_id=None, delivery_service=None):
        """Update order status and create notification"""
        old_status = self.status
        self.status = new_status
        
        # Update tracking info if provided
        if tracking_id:
            self.tracking_id = tracking_id
        if delivery_service:
            self.delivery_service = delivery_service
        
        # Set dates based on status
        from django.utils import timezone
        if new_status == 'shipped':
            self.shipped_date = timezone.now()
            if self.delivery_service:
                from datetime import timedelta
                self.estimated_delivery_date = timezone.now().date() + timedelta(days=self.delivery_service.estimated_delivery_days)
        elif new_status == 'delivered':
            self.actual_delivery_date = timezone.now()
        
        self.save()
        
        # Create notification
        notification_type = f'order_{new_status}'
        title = f"Order #{self.id} Status Updated"
        message = f"Your order status has been updated to: {self.get_status_display()}"
        
        if new_status == 'shipped' and self.tracking_id:
            message += f"\nTracking ID: {self.tracking_id}"
            if self.tracking_url:
                message += f"\nTrack your order: {self.tracking_url}"
        
        Notification.objects.create(
            user=self.user,
            notification_type=notification_type,
            title=title,
            message=message,
            order=self
        ).send_email_notification()

    def create_order_notification(self):
        """Create initial order notification"""
        title = f"Order #{self.id} Confirmed"
        message = f"Thank you for your order! We've received your order and will process it soon.\nOrder Total: Rs {self.total_amount}"
        
        notification = Notification.objects.create(
            user=self.user,
            notification_type='order_created',
            title=title,
            message=message,
            order=self
        )
        notification.send_email_notification()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Ensure price is set if not provided
        if self.price is None:
            self.price = self.product.discounted_price
        # Ensure quantity is set if not provided
        if self.quantity is None:
            self.quantity = 1
        super().save(*args, **kwargs)
    
    @property
    def subtotal(self):
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity
        
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        color_info = f" ({self.color.name})" if self.color else ""
        return f"{self.quantity}x {self.product.name}{color_info} in Order #{self.order.id}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved'),
        ],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
