from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from store.models import Product, Category
from inventory_erp.models import Purchase, PurchaseItem, Dealer
from decimal import Decimal

class PurchaseItemModelTest(TestCase):
    def setUp(self):
        current_time = timezone.now()
        
        # Create test dealer
        self.dealer = Dealer.objects.create(
            name="Test Dealer",
            dealer_type="main",
            credit_limit=Decimal('10000.00')
        )
        
        # Create test purchase
        self.purchase = Purchase.objects.create(
            dealer=self.dealer,
            total_amount=Decimal('0.00'),
            purchase_date=current_time,
            payment_due_date=current_time + timedelta(days=30)
        )
        
        # Create test category
        self.category = Category.objects.create(
            name="Mobile Phones"
        )
        
        # Create test product
        self.product = Product.objects.create(
            name="Test Phone",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )

    def test_total_price_calculation(self):
        purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase,
            product=self.product,
            quantity=2,
            unit_price=Decimal('500.00')
        )
        self.assertEqual(purchase_item.total_price, Decimal('1000.00'))

    def test_total_price_with_zero_quantity(self):
        purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase,
            product=self.product,
            quantity=0,
            unit_price=Decimal('500.00')
        )
        self.assertEqual(purchase_item.total_price, Decimal('0'))
