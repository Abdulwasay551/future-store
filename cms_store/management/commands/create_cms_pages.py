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
        blog_index = None
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
        else:
            # Get existing blog index
            blog_index = BlogIndexPage.objects.first()
            
        # Always create blog categories, tags, and posts if blog_index exists
        if blog_index:
            
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
            tags_data = ['smartphone', 'android', 'ios', 'review', 'tips', 'technology', 'mobile', 'apps', 'battery', 'security', 'maintenance', 'buying-guide', 'comparison', 'budget', 'flagship', 'camera', 'gaming', 'productivity', 'accessories']
            blog_tags = []
            for tag_name in tags_data:
                from django.utils.text import slugify
                tag, created = BlogTag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': slugify(tag_name)}
                )
                blog_tags.append(tag)
            
            # Create Comprehensive Blog Posts
            posts_data = [
                # Buying Guides
                {
                    'title': 'How to Choose the Right Smartphone: Complete Buyer\'s Guide 2024',
                    'slug': 'how-to-choose-right-smartphone-complete-guide',
                    'excerpt': 'Everything you need to know before buying your next smartphone - from budget considerations to technical specifications.',
                    'content': '<p>Choosing the perfect smartphone can be overwhelming with hundreds of options available. This comprehensive guide will help you make an informed decision based on your needs, budget, and preferences.</p><h2>1. Determine Your Budget</h2><p>Set a realistic budget range. Consider that expensive doesn\'t always mean better for your specific needs. Great phones are available in every price segment.</p><h2>2. Operating System Choice</h2><p>Decide between iOS and Android based on your ecosystem preferences and technical comfort level.</p><h2>3. Essential Features to Consider</h2><ul><li><strong>Display:</strong> Size, resolution, refresh rate</li><li><strong>Camera:</strong> Megapixels, number of lenses, night mode</li><li><strong>Battery:</strong> Capacity, fast charging support</li><li><strong>Storage:</strong> Internal storage and expandability</li><li><strong>Performance:</strong> Processor, RAM for your usage patterns</li></ul><h2>4. Research and Compare</h2><p>Read reviews, compare specifications, and if possible, test the phone in-store before making your final decision.</p><h2>5. Consider After-Sales Support</h2><p>Check warranty terms, service center availability, and brand reputation for customer support in Pakistan.</p>',
                    'category': blog_categories[2],  # Buying Guide
                    'featured_image': 'https://via.placeholder.com/800x450/6366F1/FFFFFF?text=Smartphone+Buying+Guide',
                    'author_name': 'Mobile Consultant',
                    'is_featured': True,
                    'tags': ['buying-guide', 'smartphone', 'tips', 'technology']
                },
                {
                    'title': 'Android vs iOS: Which Operating System is Better for You?',
                    'slug': 'android-vs-ios-which-operating-system-better',
                    'excerpt': 'Detailed comparison of Android and iOS to help you choose the right mobile operating system for your needs.',
                    'content': '<p>The eternal debate: Android or iOS? Both have their strengths and weaknesses. Let\'s break down the key differences to help you make the right choice for your lifestyle and preferences.</p><h2>Customization and Flexibility</h2><p><strong>Android Wins:</strong> Android offers extensive customization options. You can change launchers, install apps from multiple sources, and modify almost every aspect of your phone\'s interface.</p><p><strong>iOS:</strong> Limited customization but offers a consistent, polished experience across all devices.</p><h2>App Ecosystem</h2><p><strong>iOS:</strong> Apps often launch first on iOS, generally higher quality control, and better optimization for the platform.</p><p><strong>Android:</strong> Larger variety of apps, including more free options and alternative app stores.</p><h2>Hardware Variety</h2><p><strong>Android:</strong> Massive selection from budget to premium, different sizes, features, and price points.</p><p><strong>iOS:</strong> Limited to Apple devices but guaranteed quality and long-term software support.</p><h2>Privacy and Security</h2><p><strong>iOS:</strong> Generally considered more secure with better privacy controls and longer security update support.</p><p><strong>Android:</strong> Google has improved security significantly, but update consistency varies by manufacturer.</p><h2>Integration and Ecosystem</h2><p><strong>iOS:</strong> Seamless integration with Mac, iPad, Apple Watch, and other Apple products.</p><p><strong>Android:</strong> Better integration with Google services and more flexibility with third-party services.</p><h2>The Verdict</h2><p>Choose iOS if you want simplicity, security, and seamless ecosystem integration. Choose Android if you prefer customization, variety, and flexibility.</p>',
                    'category': blog_categories[2],  # Buying Guide
                    'featured_image': 'https://via.placeholder.com/800x450/FF3B30/FFFFFF?text=Android+vs+iOS',
                    'author_name': 'OS Expert',
                    'is_featured': True,
                    'tags': ['android', 'ios', 'comparison', 'buying-guide']
                },
                {
                    'title': '10 Proven Battery Optimization Tips to Extend Your Phone\'s Life',
                    'slug': '10-proven-battery-optimization-tips-extend-phone-life',
                    'excerpt': 'Expert-tested methods to maximize your smartphone battery life and improve daily usage time.',
                    'content': '<p>Battery life is one of the most common smartphone complaints. These scientifically-backed tips will help you squeeze every hour out of your phone\'s battery and extend its overall lifespan.</p><h2>Display Settings Optimization</h2><ul><li><strong>Reduce Screen Brightness:</strong> Use automatic brightness or keep it at 50% or lower</li><li><strong>Shorter Screen Timeout:</strong> Set to 30 seconds or 1 minute</li><li><strong>Dark Mode:</strong> Use dark themes, especially on OLED displays</li><li><strong>Reduce Refresh Rate:</strong> Switch from 120Hz to 60Hz if available</li></ul><h2>Background App Management</h2><ul><li>Disable background refresh for unnecessary apps</li><li>Close apps you\'re not actively using</li><li>Turn off location services for apps that don\'t need it</li></ul><h2>Connectivity Tweaks</h2><ul><li><strong>WiFi Over Cellular:</strong> Use WiFi whenever possible</li><li><strong>Airplane Mode:</strong> Use in low signal areas to prevent battery drain</li><li><strong>Bluetooth:</strong> Turn off when not in use</li><li><strong>Hotspot:</strong> Disable when not sharing internet</li></ul><h2>Advanced Battery Tips</h2><ul><li>Enable low power mode when battery drops below 20%</li><li>Keep your phone between 20-80% charge for optimal battery health</li><li>Avoid extreme temperatures</li><li>Use original or certified chargers</li></ul>',
                    'category': blog_categories[3],  # Tips & Tricks
                    'featured_image': 'https://via.placeholder.com/800x450/10B981/FFFFFF?text=Battery+Optimization',
                    'author_name': 'Battery Expert',
                    'is_featured': True,
                    'tags': ['battery', 'tips', 'optimization', 'smartphone']
                }
            ]
            
            # Only create blog posts if none exist yet
            if BlogPost.objects.count() == 0:
                for post_data in posts_data:
                    tags = post_data.pop('tags', [])
                    excerpt = post_data.get('excerpt', '')
                    post = BlogPost(
                        **post_data,
                        # SEO fields
                        search_description=excerpt,
                        keywords=', '.join(tags),
                    )
                    blog_index.add_child(instance=post)
                    post.save()
                    
                    # Add tags to the post
                    for tag_name in tags:
                        tag = next((t for t in blog_tags if t.name == tag_name), None)
                        if tag:
                            post.tags.add(tag)
                    
                    self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))
            else:
                self.stdout.write(self.style.WARNING('Blog posts already exist, skipping creation.'))

        self.stdout.write(self.style.SUCCESS('Initial CMS pages created successfully with sample content and SEO optimization!'))