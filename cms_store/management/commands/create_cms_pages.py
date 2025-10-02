from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from cms_store.models import (
    HomePage, AboutPage, ContactPage, BlogIndexPage, BlogPost, BlogCategory, BlogTag,
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
                hero_description='Leading Mobile Technology Hub in Bahawalpur',
                
                # Statistics
                stats_customers_count=10000,
                stats_customers_label='Happy Customers',
                stats_products_count=25000,
                stats_products_label='Devices Sold',
                stats_years_experience=12,
                stats_years_label='Years Experience',
                stats_support_text='99%',
                stats_support_label='Service Rate',
                
                # Mission & Vision
                mission_title='Our Mission',
                mission_content='<p>To provide cutting-edge mobile technology solutions that enhance connectivity and productivity for our customers while maintaining the highest standards of service and authenticity.</p>',
                vision_title='Our Vision',
                vision_content='<p>To be the most trusted and preferred destination for mobile technology in Punjab, known for innovation, quality, and exceptional customer experience.</p>',
                
                # Location Section
                location_title='Visit Our Store',
                location_description='Located in the heart of Bahawalpur, our modern showroom offers a comprehensive range of mobile devices and accessories.',
                location_phone1='+92 300 9681212',
                location_phone2='+92 315 9682684',
                location_email='mobilercornerbwp@gmail.com',
                location_address='Dubai Plaza, shop#13 basement, Bahawalpur, 63100',
                hours_monday_thursday='11:00 AM - 11:00 PM',
                hours_saturday_sunday='12:00 PM - 11:00 PM',
                hours_friday='Closed',
                
                # CTA Section
                cta_title='READY TO EXPERIENCE THE DIFFERENCE?',
                cta_description='Join thousands of satisfied customers who have made Mobile Corner their trusted tech partner.',
                cta_button1_text='SHOP NOW',
                cta_button1_url='https://mobilecorner.pk/store/',
                cta_button2_text='CONTACT US',
                cta_button2_url='https://mobilecorner.pk/contact/',
                
                # SEO fields
                search_description='Learn about Mobile Corner Bahawalpur - Your trusted mobile technology partner with 12+ years of experience, 10,000+ happy customers, and premium device selection.',
                keywords='about mobile corner, mobile shop bahawalpur, mobile store history, trusted mobile retailer, mobile corner story',
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

        # Create Blog Section
        if home_page and not BlogIndexPage.objects.exists():            
            # Create Blog Index Page
            blog_index = BlogIndexPage(
                title='Tech Blog',
                slug='blog',
                hero_title='TECH BLOG',
                hero_description='Stay updated with the latest mobile technology trends, reviews, and insights from our experts.',
                # SEO fields
                search_description='Mobile Corner Tech Blog - Latest smartphone reviews, mobile technology trends, buying guides, and expert insights from Bahawalpur\'s premier mobile store.',
                keywords='mobile blog, smartphone reviews, tech trends, mobile technology, buying guides, mobile corner blog',
            )
            home_page.add_child(instance=blog_index)
            self.stdout.write(self.style.SUCCESS(f'Created blog index: {blog_index.title}'))
            
            # Create Blog Categories
            categories_data = [
                {'name': 'Reviews', 'slug': 'reviews', 'description': 'In-depth smartphone and device reviews'},
                {'name': 'Tech News', 'slug': 'tech-news', 'description': 'Latest technology news and updates'},
                {'name': 'Buying Guide', 'slug': 'buying-guide', 'description': 'Help choosing the right device'},
                {'name': 'Tips & Tricks', 'slug': 'tips-tricks', 'description': 'Mobile tips and optimization guides'}
            ]
            
            blog_categories = []
            for cat_data in categories_data:
                category, created = BlogCategory.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={
                        'slug': cat_data['slug'],
                        'description': cat_data['description']
                    }
                )
                blog_categories.append(category)
            
            # Create Blog Tags
            tags_data = ['smartphone', 'android', 'ios', 'review', 'tips', 'technology', 'mobile', 'apps']
            blog_tags = []
            for tag_name in tags_data:
                tag, created = BlogTag.objects.get_or_create(name=tag_name)
                blog_tags.append(tag)
            
            # Create Sample Blog Posts
            posts_data = [
                {
                    'title': 'iPhone 15 Pro Max vs Samsung Galaxy S24 Ultra: The Ultimate Comparison',
                    'slug': 'iphone-15-pro-max-vs-samsung-galaxy-s24-ultra',
                    'excerpt': 'Detailed comparison of the two flagship smartphones that dominate the premium market in 2024.',
                    'intro': '<p>In the premium smartphone segment, two devices stand out as the clear leaders: Apple\'s iPhone 15 Pro Max and Samsung\'s Galaxy S24 Ultra. Both offer cutting-edge technology, but which one offers better value for Pakistani consumers?</p>',
                    'body': '<h2>Design and Build Quality</h2><p>Both phones feature premium materials and excellent build quality. The iPhone 15 Pro Max sports a titanium frame with ceramic shield glass, while the Galaxy S24 Ultra uses an aluminum frame with Gorilla Glass Victus 2.</p><h2>Performance Comparison</h2><p>The iPhone 15 Pro Max is powered by the A17 Pro chip, while the Galaxy S24 Ultra runs on the Snapdragon 8 Gen 3. Both offer flagship-level performance for demanding tasks.</p><h2>Camera Systems</h2><p>Photography enthusiasts will find both phones excellent, with the iPhone excelling in video recording and the Galaxy offering more versatility with its zoom capabilities.</p>',
                    'category': blog_categories[0],  # Reviews
                    'featured_image_url': 'https://via.placeholder.com/800x450/007AFF/FFFFFF?text=iPhone+vs+Samsung',
                    'author': 'Tech Expert Team',
                    'is_featured': True,
                    'tags': ['smartphone', 'review', 'ios', 'android']
                },
                {
                    'title': '5 Essential Android Tips Every User Should Know',
                    'slug': '5-essential-android-tips-every-user-should-know',
                    'excerpt': 'Unlock your Android phone\'s potential with these simple but powerful tips and tricks.',
                    'intro': '<p>Android phones offer incredible flexibility and customization options. Here are five essential tips that will help you get the most out of your Android device.</p>',
                    'body': '<h2>1. Master Your Battery Settings</h2><p>Learn how to optimize your battery life with adaptive battery settings and background app limitations.</p><h2>2. Customize Your Home Screen</h2><p>Make your phone truly yours with widgets, custom launchers, and icon packs.</p><h2>3. Use Google Assistant Effectively</h2><p>Voice commands and automation can save you time throughout the day.</p>',
                    'category': blog_categories[3],  # Tips & Tricks
                    'featured_image_url': 'https://via.placeholder.com/800x450/34A853/FFFFFF?text=Android+Tips',
                    'author': 'Mobile Expert',
                    'is_featured': True,
                    'tags': ['android', 'tips', 'mobile']
                },
                {
                    'title': 'Best Budget Smartphones Under PKR 50,000 in 2024',
                    'slug': 'best-budget-smartphones-under-pkr-50000-2024',
                    'excerpt': 'Find the perfect smartphone that offers great value without breaking the bank.',
                    'intro': '<p>You don\'t need to spend a fortune to get a great smartphone. Here are our top picks for budget-friendly phones under PKR 50,000 that deliver excellent performance and features.</p>',
                    'body': '<h2>Xiaomi Redmi Note 13 Pro</h2><p>Excellent camera system and fast charging at an affordable price point.</p><h2>Realme 11 Pro</h2><p>Great design and solid performance for everyday tasks and gaming.</p><h2>Samsung Galaxy A54</h2><p>Reliable performance with Samsung\'s ecosystem integration.</p>',
                    'category': blog_categories[2],  # Buying Guide
                    'featured_image_url': 'https://via.placeholder.com/800x450/FF6B6B/FFFFFF?text=Budget+Phones',
                    'author': 'Pricing Expert',
                    'tags': ['smartphone', 'buying-guide', 'budget']
                }
            ]
            
            for post_data in posts_data:
                tags = post_data.pop('tags', [])
                post = BlogPost(
                    **post_data,
                    # SEO fields
                    search_description=post_data['excerpt'],
                    keywords=', '.join(tags),
                )
                blog_index.add_child(instance=post)
                
                # Add tags to the post
                for tag_name in tags:
                    tag = next((t for t in blog_tags if t.name == tag_name), None)
                    if tag:
                        post.tags.add(tag)
                
                self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))

        self.stdout.write(self.style.SUCCESS('Initial CMS pages created successfully with sample content and SEO optimization!'))