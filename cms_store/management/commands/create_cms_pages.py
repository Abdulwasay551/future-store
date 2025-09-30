from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from cms_store.models import (
    HomePage, AboutPage, ContactPage, 
    HeroButton, FeatureItem, CertificationItem, BrandLogo, 
    GalleryImage, WhyChooseUsItem, Testimonial
)


class Command(BaseCommand):
    help = 'Create initial CMS pages with sample content'

    def handle(self, *args, **options):
        # Import Site model here to avoid circular imports
        from wagtail.models import Site, Page
        
        # Get or create the default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(self.style.ERROR('No default site found. Please run Wagtail migrations first.'))
            return

        root_page = site.root_page

        # Create Home Page
        if not HomePage.objects.exists():
            home_page = HomePage(
                title='Home',
                slug='home',
                hero_main_title='MOBILE CORNER',
                hero_subtitle_line1='Your Premium Destination for Mobile Technology',
                hero_subtitle_line2='Experience Excellence in Every Device',
                # SEO fields
                search_description='Mobile Corner - Your trusted partner for premium mobile devices, smartphones, and technology solutions in Bahawalpur.',
                keywords='mobile phones, smartphones, mobile corner, bahawalpur, mobile shop, premium devices',
            )
            root_page.add_child(instance=home_page)
            
            # Set as the site's root page
            site.root_page = home_page
            site.save()
            
            self.stdout.write(self.style.SUCCESS(f'Created home page: {home_page.title}'))
            
            # Add sample hero buttons
            HeroButton.objects.create(
                page=home_page,
                text='Explore Products',
                url='/store/',
                is_primary=True,
                order=1
            )
            HeroButton.objects.create(
                page=home_page,
                text='Contact Us',
                url='/contact/',
                is_primary=False,
                order=2
            )
            
            # Add sample features
            features_data = [
                {
                    'icon_class': 'fas fa-shield-alt',
                    'title': 'Authentic Products',
                    'description': 'We guarantee 100% authentic products from official distributors.',
                    'order': 1
                },
                {
                    'icon_class': 'fas fa-shipping-fast',
                    'title': 'Fast Delivery',
                    'description': 'Quick and secure delivery across Pakistan.',
                    'order': 2
                },
                {
                    'icon_class': 'fas fa-tools',
                    'title': 'Expert Support',
                    'description': '24/7 technical support and after-sales service.',
                    'order': 3
                },
                {
                    'icon_class': 'fas fa-medal',
                    'title': 'Best Prices',
                    'description': 'Competitive prices with regular discounts and offers.',
                    'order': 4
                }
            ]
            
            for feature_data in features_data:
                FeatureItem.objects.create(page=home_page, **feature_data)

        # Create About Page
        home_page = HomePage.objects.first()
        if home_page and not AboutPage.objects.exists():
            about_page = AboutPage(
                title='About Us',
                slug='about',
                hero_title_part1='ABOUT',
                hero_title_part2='MOBILE CORNER',
                hero_description='Your trusted partner in mobile technology since day one',
                story_content='<p>Mobile Corner has been serving customers in Bahawalpur for over a decade, providing premium mobile devices and exceptional service. We pride ourselves on offering authentic products, competitive prices, and unmatched customer support.</p>',
                mission_content='<p>To provide our customers with the latest mobile technology at competitive prices while ensuring exceptional service and support.</p>',
                vision_content='<p>To become the leading mobile technology retailer in the region, known for trust, quality, and innovation.</p>',
                # SEO fields
                search_description='Learn about Mobile Corner - Bahawalpur\'s trusted mobile phone store with over 10 years of experience in mobile technology.',
                keywords='mobile corner about, mobile shop bahawalpur, mobile store history, authentic mobile phones',
            )
            home_page.add_child(instance=about_page)
            self.stdout.write(self.style.SUCCESS(f'Created about page: {about_page.title}'))
            
            # Add sample certifications
            certifications_data = [
                {
                    'icon_class': 'fas fa-certificate',
                    'title': 'Samsung Authorized Dealer',
                    'description': 'Official Samsung products with warranty',
                    'order': 1
                },
                {
                    'icon_class': 'fab fa-apple',
                    'title': 'Apple Premium Partner',
                    'description': 'Authorized Apple iPhone retailer',
                    'order': 2
                },
                {
                    'icon_class': 'fas fa-award',
                    'title': 'ISO 9001 Certified',
                    'description': 'Quality management system certified',
                    'order': 3
                }
            ]
            
            for cert_data in certifications_data:
                CertificationItem.objects.create(page=about_page, **cert_data)
            
            # Add sample brand logos
            brands_data = [
                {'name': 'Samsung', 'logo_url': '/static/samsung-logo.png', 'order': 1},
                {'name': 'Apple', 'logo_url': '/static/apple-logo.png', 'order': 2},
                {'name': 'Xiaomi', 'logo_url': '/static/xiaomi-logo.png', 'order': 3},
                {'name': 'OnePlus', 'logo_url': '/static/oneplus-logo.png', 'order': 4},
                {'name': 'OPPO', 'logo_url': '/static/oppo-logo.png', 'order': 5},
                {'name': 'Vivo', 'logo_url': '/static/vivo-logo.png', 'order': 6},
            ]
            
            for brand_data in brands_data:
                BrandLogo.objects.create(page=about_page, **brand_data)
            
            # Add sample gallery images
            gallery_data = [
                {
                    'title': 'Store Front',
                    'image_url': '/static/about (1).jpg',
                    'description': 'Our main store location in Bahawalpur',
                    'order': 1
                },
                {
                    'title': 'Interior View',
                    'image_url': '/static/about (2).jpg',
                    'description': 'Modern and organized product display',
                    'order': 2
                },
                {
                    'title': 'Service Center',
                    'image_url': '/static/about (3).jpg',
                    'description': 'Professional repair and service facility',
                    'order': 3
                },
                {
                    'title': 'Customer Area',
                    'image_url': '/static/about (4).jpg',
                    'description': 'Comfortable customer consultation area',
                    'order': 4
                }
            ]
            
            for gallery_data in gallery_data:
                GalleryImage.objects.create(page=about_page, **gallery_data)
            
            # Add why choose us items
            why_choose_data = [
                {
                    'icon_class': 'fas fa-handshake',
                    'title': 'Trusted Service',
                    'description': 'Over 10 years of reliable service in Bahawalpur',
                    'order': 1
                },
                {
                    'icon_class': 'fas fa-dollar-sign',
                    'title': 'Best Prices',
                    'description': 'Competitive pricing with regular promotions',
                    'order': 2
                },
                {
                    'icon_class': 'fas fa-users',
                    'title': 'Expert Team',
                    'description': 'Knowledgeable staff to help you choose the right device',
                    'order': 3
                },
                {
                    'icon_class': 'fas fa-wrench',
                    'title': 'After-Sales Support',
                    'description': 'Complete support and service after your purchase',
                    'order': 4
                }
            ]
            
            for item_data in why_choose_data:
                WhyChooseUsItem.objects.create(page=about_page, **item_data)
            
            # Add sample testimonials
            testimonials_data = [
                {
                    'name': 'Ahmed Ali',
                    'designation': 'Business Owner',
                    'testimonial_text': 'Mobile Corner provided excellent service when I bought my iPhone. Great prices and authentic products!',
                    'rating': 5,
                    'order': 1
                },
                {
                    'name': 'Sarah Khan',
                    'designation': 'Student',
                    'testimonial_text': 'Best mobile shop in Bahawalpur. They helped me find the perfect smartphone within my budget.',
                    'rating': 5,
                    'order': 2
                },
                {
                    'name': 'Muhammad Hassan',
                    'designation': 'Engineer',
                    'testimonial_text': 'Professional service and genuine products. I have been their customer for years.',
                    'rating': 5,
                    'order': 3
                }
            ]
            
            for testimonial_data in testimonials_data:
                Testimonial.objects.create(page=about_page, **testimonial_data)

        # Create Contact Page
        if home_page and not ContactPage.objects.exists():
            contact_page = ContactPage(
                title='Contact',
                slug='contact',
                page_title_part1='GET IN',
                page_title_part2='TOUCH',
                page_description="Have questions? We'd love to hear from you.",
                # SEO fields
                search_description='Contact Mobile Corner Bahawalpur - Visit our store, call us, or send us a message for mobile phone inquiries and support.',
                keywords='mobile corner contact, bahawalpur mobile shop contact, mobile phone store location, phone number',
            )
            home_page.add_child(instance=contact_page)
            self.stdout.write(self.style.SUCCESS(f'Created contact page: {contact_page.title}'))

        self.stdout.write(self.style.SUCCESS('Initial CMS pages created successfully with sample content and SEO optimization!'))