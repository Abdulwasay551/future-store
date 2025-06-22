from django.core.management.base import BaseCommand
from store.models import Category, Company, Product, ProductColor, ProductImage
from decimal import Decimal
import json

class Command(BaseCommand):
    help = 'Populate sample products with new JSON format features and specs'

    def handle(self, *args, **options):
        # Create or get category
        category, created = Category.objects.get_or_create(
            name='Smartphones',
            defaults={
                'slug': 'smartphones',
                'description': 'Latest smartphones and mobile devices'
            }
        )
        
        # Create or get company
        company, created = Company.objects.get_or_create(
            name='Samsung',
            defaults={
                'slug': 'samsung',
                'category': category,
                'description': 'Leading smartphone manufacturer'
            }
        )

        # Sample features and specs data
        samsung_s10_features = {
            "device": "Samsung Galaxy S10",
            "features": [
                "Infinity-O Dynamic AMOLED Display",
                "Ultrasonic Fingerprint Scanner",
                "Triple Rear Camera Setup",
                "Wireless PowerShare (reverse wireless charging)",
                "Water and Dust Resistance (IP68)",
                "Fast Wireless Charging 2.0",
                "Samsung Knox Security",
                "One UI Interface",
                "Expandable Storage via microSD",
                "Face Recognition"
            ]
        }

        samsung_s10_specs = {
            "device": "Samsung Galaxy S10",
            "specifications": {
                "display": {
                    "type": "Dynamic AMOLED",
                    "size": "6.1 inches",
                    "resolution": "1440 x 3040 pixels",
                    "protection": "Corning Gorilla Glass 6"
                },
                "platform": {
                    "os": "Android 9.0 (Pie), upgradable",
                    "chipset": "Exynos 9820 (EMEA) / Snapdragon 855 (USA)",
                    "cpu": "Octa-core",
                    "gpu": "Mali-G76 MP12 / Adreno 640"
                },
                "memory": {
                    "ram": "8 GB",
                    "internal_storage": "128/512 GB",
                    "expandable": "microSD up to 1 TB"
                },
                "camera": {
                    "rear": "12 MP (wide) + 12 MP (telephoto) + 16 MP (ultrawide)",
                    "front": "10 MP"
                },
                "battery": {
                    "capacity": "3400 mAh",
                    "charging": "15W wired, 15W wireless, reverse wireless charging"
                },
                "build": {
                    "dimensions": "149.9 x 70.4 x 7.8 mm",
                    "weight": "157 g",
                    "protection": "IP68 dust/water resistant"
                },
                "connectivity": {
                    "usb": "USB Type-C 3.1",
                    "bluetooth": "5.0",
                    "wifi": "Wi-Fi 802.11 a/b/g/n/ac/ax"
                }
            }
        }

        # Create or update Samsung Galaxy S10
        product, created = Product.objects.get_or_create(
            name='Samsung Galaxy S10',
            defaults={
                'slug': 'samsung-galaxy-s10',
                'category': category,
                'company': company,
                'description': 'Experience the future of mobile technology with the Samsung Galaxy S10. Featuring an Infinity-O Dynamic AMOLED display, ultrasonic fingerprint scanner, and triple rear camera setup.',
                'price': Decimal('899.99'),
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'is_available': True,
                'is_featured': True,
                'features': samsung_s10_features,
                'specs': samsung_s10_specs
            }
        )

        if not created:
            product.features = samsung_s10_features
            product.specs = samsung_s10_specs
            product.save()

        # Create colors for Samsung Galaxy S10
        colors_data = [
            {'name': 'Prism White', 'hex_code': '#FFFFFF', 'stock': 15, 'is_primary': True},
            {'name': 'Prism Black', 'hex_code': '#000000', 'stock': 20, 'is_primary': False},
            {'name': 'Prism Blue', 'hex_code': '#0066CC', 'stock': 12, 'is_primary': False},
            {'name': 'Prism Green', 'hex_code': '#00CC66', 'stock': 8, 'is_primary': False},
        ]

        for color_data in colors_data:
            color, created = ProductColor.objects.get_or_create(
                product=product,
                name=color_data['name'],
                defaults={
                    'hex_code': color_data['hex_code'],
                    'stock': color_data['stock'],
                    'is_primary': color_data['is_primary']
                }
            )
            if not created:
                color.hex_code = color_data['hex_code']
                color.stock = color_data['stock']
                color.is_primary = color_data['is_primary']
                color.save()

        # Create iPhone 13 Pro sample
        iphone_features = {
            "device": "iPhone 13 Pro",
            "features": [
                "ProMotion 120Hz Display",
                "A15 Bionic Chip",
                "Pro Camera System with 3x Telephoto",
                "Cinematic Mode",
                "ProRes Video Recording",
                "Ceramic Shield Protection",
                "Face ID",
                "MagSafe Charging",
                "5G Capable",
                "iOS 15"
            ]
        }

        iphone_specs = {
            "device": "iPhone 13 Pro",
            "specifications": {
                "display": {
                    "type": "Super Retina XDR OLED",
                    "size": "6.1 inches",
                    "resolution": "1170 x 2532 pixels",
                    "protection": "Ceramic Shield"
                },
                "platform": {
                    "os": "iOS 15",
                    "chipset": "Apple A15 Bionic",
                    "cpu": "Hexa-core",
                    "gpu": "Apple GPU (5-core graphics)"
                },
                "memory": {
                    "ram": "6 GB",
                    "internal_storage": "128/256/512 GB/1 TB",
                    "expandable": "No"
                },
                "camera": {
                    "rear": "12 MP (wide) + 12 MP (telephoto) + 12 MP (ultrawide)",
                    "front": "12 MP"
                },
                "battery": {
                    "capacity": "3095 mAh",
                    "charging": "20W wired, 15W MagSafe, 7.5W Qi wireless"
                },
                "build": {
                    "dimensions": "146.7 x 71.5 x 7.7 mm",
                    "weight": "203 g",
                    "protection": "IP68 dust/water resistant"
                },
                "connectivity": {
                    "usb": "Lightning",
                    "bluetooth": "5.0",
                    "wifi": "Wi-Fi 802.11 a/b/g/n/ac/6"
                }
            }
        }

        # Create iPhone company
        apple_company, created = Company.objects.get_or_create(
            name='Apple',
            defaults={
                'slug': 'apple',
                'category': category,
                'description': 'Premium technology company'
            }
        )

        iphone_product, created = Product.objects.get_or_create(
            name='iPhone 13 Pro',
            defaults={
                'slug': 'iphone-13-pro',
                'category': category,
                'company': apple_company,
                'description': 'The most advanced iPhone ever. Featuring Pro camera system, A15 Bionic chip, and ProMotion display.',
                'price': Decimal('999.99'),
                'discount_type': 'none',
                'discount_value': Decimal('0.00'),
                'is_available': True,
                'is_featured': True,
                'features': iphone_features,
                'specs': iphone_specs
            }
        )

        if not created:
            iphone_product.features = iphone_features
            iphone_product.specs = iphone_specs
            iphone_product.save()

        # Create colors for iPhone 13 Pro
        iphone_colors = [
            {'name': 'Sierra Blue', 'hex_code': '#5E8B7E', 'stock': 18, 'is_primary': True},
            {'name': 'Silver', 'hex_code': '#C0C0C0', 'stock': 22, 'is_primary': False},
            {'name': 'Gold', 'hex_code': '#FFD700', 'stock': 15, 'is_primary': False},
            {'name': 'Graphite', 'hex_code': '#41424C', 'stock': 25, 'is_primary': False},
        ]

        for color_data in iphone_colors:
            color, created = ProductColor.objects.get_or_create(
                product=iphone_product,
                name=color_data['name'],
                defaults={
                    'hex_code': color_data['hex_code'],
                    'stock': color_data['stock'],
                    'is_primary': color_data['is_primary']
                }
            )
            if not created:
                color.hex_code = color_data['hex_code']
                color.stock = color_data['stock']
                color.is_primary = color_data['is_primary']
                color.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample products with new JSON format features and specs')
        ) 