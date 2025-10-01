from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey


# Base Page with SEO support
class CMSBasePage(Page):
    """Base page class for CMS pages with SEO support"""
    
    # Additional SEO Fields (seo_title and search_description are already in Page model)
    keywords = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Comma-separated keywords for SEO. e.g., mobile phones, smartphones, technology"
    )
    canonical_url = models.URLField(
        blank=True, 
        help_text="Optional canonical URL to prevent duplicate content issues"
    )
    og_title = models.CharField(
        max_length=95, 
        blank=True, 
        help_text="Title for social media sharing (Open Graph). Maximum 95 characters."
    )
    og_description = models.TextField(
        max_length=200, 
        blank=True, 
        help_text="Description for social media sharing. Maximum 200 characters."
    )
    og_image = models.URLField(
        blank=True, 
        help_text="Image URL for social media sharing (1200x630px recommended)"
    )
    
    # Analytics
    google_analytics_id = models.CharField(
        max_length=20, 
        blank=True, 
        help_text="Google Analytics ID (e.g., GA_MEASUREMENT_ID)"
    )
    facebook_pixel_id = models.CharField(
        max_length=20, 
        blank=True, 
        help_text="Facebook Pixel ID"
    )
    
    # Additional SEO options
    noindex = models.BooleanField(
        default=False, 
        help_text="Prevent search engines from indexing this page"
    )
    nofollow = models.BooleanField(
        default=False, 
        help_text="Prevent search engines from following links on this page"
    )
    
    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('keywords'),
            FieldPanel('canonical_url'),
        ], heading='Additional SEO'),
        MultiFieldPanel([
            FieldPanel('og_title'),
            FieldPanel('og_description'),
            FieldPanel('og_image'),
        ], heading='Social Media (Open Graph)'),
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('facebook_pixel_id'),
        ], heading='Analytics & Tracking'),
        MultiFieldPanel([
            FieldPanel('noindex'),
            FieldPanel('nofollow'),
        ], heading='Search Engine Directives'),
    ]
    
    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        # Remove references to store models - CMS only handles static content
        return context

    def get_meta_title(self):
        """Return the SEO title if available, otherwise the page title"""
        return self.seo_title if self.seo_title else self.title

    def get_meta_description(self):
        """Return the meta description"""
        return self.search_description

    def get_meta_keywords(self):
        """Return the meta keywords"""
        return self.keywords

    def get_og_title(self):
        """Return the Open Graph title"""
        return self.og_title if self.og_title else self.get_meta_title()

    def get_og_description(self):
        """Return the Open Graph description"""
        return self.og_description if self.og_description else self.get_meta_description()

    def get_canonical_url(self):
        """Return the canonical URL"""
        return self.canonical_url if self.canonical_url else self.get_full_url()


# Inline models for reusable content blocks
class HeroButton(models.Model):
    """Reusable hero buttons"""
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='hero_buttons')
    text = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('text'),
        FieldPanel('url'),
        FieldPanel('is_primary'),
        FieldPanel('order'),
    ]


class FeatureItem(models.Model):
    """Features section items"""
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='features')
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class (e.g., fas fa-shield-alt)")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('icon_class'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('order'),
    ]


class CertificationItem(models.Model):
    """Certifications for about page"""
    page = ParentalKey('AboutPage', on_delete=models.CASCADE, related_name='certifications')
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class")
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True, help_text="Optional certification image URL")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('icon_class'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image_url'),
        FieldPanel('order'),
    ]


class BrandLogo(models.Model):
    """Brand logos for about page"""
    page = ParentalKey('AboutPage', on_delete=models.CASCADE, related_name='brand_logos')
    name = models.CharField(max_length=100)
    logo_url = models.URLField(help_text="Brand logo image URL")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('name'),
        FieldPanel('logo_url'),
        FieldPanel('order'),
    ]


class GalleryImage(models.Model):
    """Gallery images for about page"""
    page = ParentalKey('AboutPage', on_delete=models.CASCADE, related_name='gallery_images')
    title = models.CharField(max_length=100)
    image_url = models.URLField(help_text="Gallery image URL")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('title'),
        FieldPanel('image_url'),
        FieldPanel('description'),
        FieldPanel('order'),
    ]


class WhyChooseUsItem(models.Model):
    """Why choose us items for about page"""
    page = ParentalKey('AboutPage', on_delete=models.CASCADE, related_name='why_choose_us_items')
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('icon_class'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('order'),
    ]


class Testimonial(models.Model):
    """Customer testimonials"""
    page = ParentalKey('AboutPage', on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, help_text="Customer photo URL")
    testimonial_text = models.TextField()
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('name'),
        FieldPanel('designation'),
        FieldPanel('image_url'),
        FieldPanel('testimonial_text'),
        FieldPanel('rating'),
        FieldPanel('order'),
    ]


class CustomerReview(models.Model):
    """Customer reviews for testimonials section"""
    page = ParentalKey('AboutPage', on_delete=models.CASCADE, related_name='customer_reviews')
    customer_name = models.CharField(max_length=100)
    customer_image_url = models.URLField(blank=True, help_text="Customer photo URL")
    review_text = models.TextField()
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    panels = [
        FieldPanel('customer_name'),
        FieldPanel('customer_image_url'),
        FieldPanel('review_text'),
        FieldPanel('rating'),
        FieldPanel('order'),
    ]


# Home Page
class HomePage(CMSBasePage):
    """CMS Home Page - manages the main landing page content"""
    template = 'index.html'
    
    # Hero Section
    hero_main_title = models.CharField(max_length=200, default="MOBILE CORNER")
    hero_subtitle_line1 = models.CharField(max_length=200, default="Your Premium Destination for Mobile Technology")
    hero_subtitle_line2 = models.CharField(max_length=200, default="Experience Excellence in Every Device")
    hero_logo_url = models.URLField(blank=True, help_text="Hero logo image URL")
    
    # Featured Products Section
    featured_section_title = models.CharField(max_length=100, default="FEATURED PRODUCTS")
    featured_section_description = models.TextField(default="Discover our premium collection of mobile devices")
    
    # Features Section
    features_section_title = models.CharField(max_length=100, default="Why Choose Mobile Corner?")
    features_section_description = models.TextField(default="Experience the difference with our premium services")
    
    # About Section
    about_section_title = models.CharField(max_length=100, default="About Mobile Corner")
    about_section_content = RichTextField(blank=True)
    about_image_url = models.URLField(blank=True, help_text="About section image URL")
    about_video_url = models.URLField(blank=True, help_text="About section video URL")
    
    # Newsletter Section
    newsletter_title = models.CharField(max_length=100, default="Stay Updated")
    newsletter_description = models.TextField(default="Subscribe to get the latest updates on new arrivals and offers")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_main_title'),
            FieldPanel('hero_subtitle_line1'),
            FieldPanel('hero_subtitle_line2'),
            FieldPanel('hero_logo_url'),
        ], heading='Hero Section'),
        MultiFieldPanel([
            FieldPanel('featured_section_title'),
            FieldPanel('featured_section_description'),
        ], heading='Featured Products Section'),
        MultiFieldPanel([
            FieldPanel('features_section_title'),
            FieldPanel('features_section_description'),
            InlinePanel('features', label="Features"),
        ], heading='Features Section'),
        MultiFieldPanel([
            FieldPanel('about_section_title'),
            FieldPanel('about_section_content'),
            FieldPanel('about_image_url'),
            FieldPanel('about_video_url'),
        ], heading='About Section'),
        MultiFieldPanel([
            FieldPanel('newsletter_title'),
            FieldPanel('newsletter_description'),
        ], heading='Newsletter Section'),
        InlinePanel('hero_buttons', label="Hero Buttons"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_main_title'),
        index.SearchField('hero_subtitle_line1'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # This page no longer shows store products
        # Add any additional context variables here
        return context


# About Page
class AboutPage(CMSBasePage):
    """CMS About Page - manages the about us page content"""
    template = 'about_us.html'
    
    # Hero Section
    hero_title_part1 = models.CharField(max_length=100, default="ABOUT")
    hero_title_part2 = models.CharField(max_length=100, default="MOBILE CORNER")
    hero_description = models.TextField(default="Your trusted partner in mobile technology since day one")
    hero_background_video_url = models.URLField(blank=True, help_text="Hero background video URL")
    
    # Certifications Section
    certifications_title_part1 = models.CharField(max_length=100, default="Official Certifications")
    certifications_title_part2 = models.CharField(max_length=100, default="& Trust Shields")
    certifications_description = models.TextField(
        default="We are proud to be officially certified and authorized by leading mobile brands"
    )
    
    # Official Documentation Section
    documentation_title = models.CharField(max_length=100, default="Official Documentation")
    documentation_description = models.TextField(
        default="View our official certifications and authorization documents"
    )
    documentation_image1_url = models.URLField(blank=True, help_text="First documentation image URL")
    documentation_image1_title = models.CharField(max_length=100, default="Apple Authorization")
    documentation_image2_url = models.URLField(blank=True, help_text="Second documentation image URL")
    documentation_image2_title = models.CharField(max_length=100, default="Samsung Partnership")
    documentation_image3_url = models.URLField(blank=True, help_text="Third documentation image URL")
    documentation_image3_title = models.CharField(max_length=100, default="Quality Certificate")
    
    # Story Section
    story_title = models.CharField(max_length=100, default="Our Story")
    story_content = RichTextField(blank=True)
    story_video_url = models.URLField(blank=True, help_text="Company story video URL")
    
    # Partners Section
    partners_title_part1 = models.CharField(max_length=100, default="Big Clients")
    partners_title_part2 = models.CharField(max_length=100, default="& Partners")
    partners_description = models.TextField(
        default="Trusted by leading brands and thousands of satisfied customers"
    )
    
    # Stats Section
    stats_title = models.CharField(max_length=100, default="BY THE NUMBERS")
    stats_description = models.TextField(default="Our achievements speak for themselves. Here's what we've accomplished together with our amazing customers and partners.")
    stats_customers_count = models.IntegerField(default=50000)
    stats_customers_label = models.CharField(max_length=50, default="Happy Customers")
    stats_products_count = models.IntegerField(default=100000)
    stats_products_label = models.CharField(max_length=50, default="Products Sold")
    stats_years_experience = models.IntegerField(default=6)
    stats_years_label = models.CharField(max_length=50, default="Years Experience")
    stats_support_text = models.CharField(max_length=20, default="24/7")
    stats_support_label = models.CharField(max_length=50, default="Support")
    
    # Gallery Section
    gallery_title_part1 = models.CharField(max_length=100, default="OUR")
    gallery_title_part2 = models.CharField(max_length=100, default="SHOWROOM")
    gallery_description = models.TextField(default="Step inside our modern showroom and experience the future of mobile technology")
    virtual_tour_url = models.URLField(blank=True, help_text="Virtual tour URL")
    virtual_tour_button_text = models.CharField(max_length=50, default="Take Virtual Tour")
    
    # Mission & Vision
    mission_vision_title_part1 = models.CharField(max_length=100, default="OUR")
    mission_vision_title_part2 = models.CharField(max_length=100, default="MISSION")
    mission_title = models.CharField(max_length=100, default="MISSION")
    mission_content = RichTextField(default="To democratize access to premium mobile technology by providing authentic, high-quality devices and exceptional customer service that exceeds expectations. We strive to be the bridge between cutting-edge technology and the Pakistani market.")
    vision_title = models.CharField(max_length=100, default="VISION")
    vision_content = RichTextField(default="To become Pakistan's leading mobile technology retailer, known for innovation, trust, and customer-centricity. We envision a future where every Pakistani has access to the latest mobile technology to enhance their digital lifestyle.")
    
    # Why Choose Us Section
    why_choose_title_part1 = models.CharField(max_length=100, default="WHY CHOOSE")
    why_choose_title_part2 = models.CharField(max_length=100, default="MOBILE CORNER")
    why_choose_description = models.TextField(default="Experience the difference that sets us apart")
    
    # Testimonials Section
    testimonials_title_part1 = models.CharField(max_length=100, default="WHAT OUR")
    testimonials_title_part2 = models.CharField(max_length=100, default="CUSTOMERS SAY")
    testimonials_description = models.TextField(default="Real stories from real customers who have experienced the Mobile Corner difference")
    testimonials_video_url = models.URLField(blank=True, help_text="Customer testimonials video URL")
    
    # Location Section
    location_title = models.CharField(max_length=100, default="VISIT US")
    location_description = models.TextField(default="Located in the heart of Bahawalpur, our store is your gateway to the latest mobile technology. Visit us for hands-on experience with our products and personalized assistance from our expert team.")
    location_address_label = models.CharField(max_length=50, default="Address")
    location_address = models.TextField(default="Dubai Plaza, shop#13 basement, Bahawalpur, 63100")
    location_phone_label = models.CharField(max_length=50, default="Phone")
    location_phone1 = models.CharField(max_length=20, default="+92 300 9681212")
    location_phone2 = models.CharField(max_length=20, default="+92 315 9682684")
    location_email_label = models.CharField(max_length=50, default="Email")
    location_email = models.EmailField(default="mobilercornerbwp@gmail.com")
    location_hours_label = models.CharField(max_length=50, default="Business Hours")
    location_maps_url = models.URLField(blank=True, help_text="Google Maps URL")
    
    # Business Hours
    hours_monday_thursday = models.CharField(max_length=50, default="11:00 AM - 11:00 PM")
    hours_saturday_sunday = models.CharField(max_length=50, default="12:00 PM - 11:00 PM")
    hours_friday = models.CharField(max_length=50, default="Closed")
    
    # CTA Section
    cta_title = models.CharField(max_length=100, default="READY TO EXPERIENCE THE DIFFERENCE?")
    cta_description = models.TextField(default="Join thousands of satisfied customers who have made Mobile Corner their trusted tech partner.")
    cta_button1_text = models.CharField(max_length=50, default="Shop Now")
    cta_button1_url = models.URLField(blank=True, help_text="First CTA button URL")
    cta_button2_text = models.CharField(max_length=50, default="Contact Us")
    cta_button2_url = models.URLField(blank=True, help_text="Second CTA button URL")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title_part1'),
            FieldPanel('hero_title_part2'),
            FieldPanel('hero_description'),
            FieldPanel('hero_background_video_url'),
        ], heading='Hero Section'),
        MultiFieldPanel([
            FieldPanel('certifications_title_part1'),
            FieldPanel('certifications_title_part2'),
            FieldPanel('certifications_description'),
            InlinePanel('certifications', label="Certifications"),
        ], heading='Certifications Section'),
        MultiFieldPanel([
            FieldPanel('documentation_title'),
            FieldPanel('documentation_description'),
            FieldPanel('documentation_image1_url'),
            FieldPanel('documentation_image1_title'),
            FieldPanel('documentation_image2_url'),
            FieldPanel('documentation_image2_title'),
            FieldPanel('documentation_image3_url'),
            FieldPanel('documentation_image3_title'),
        ], heading='Official Documentation'),
        MultiFieldPanel([
            FieldPanel('story_title'),
            FieldPanel('story_content'),
            FieldPanel('story_video_url'),
        ], heading='Story Section'),
        MultiFieldPanel([
            FieldPanel('partners_title_part1'),
            FieldPanel('partners_title_part2'),
            FieldPanel('partners_description'),
            InlinePanel('brand_logos', label="Brand Logos"),
        ], heading='Partners Section'),
        MultiFieldPanel([
            FieldPanel('stats_title'),
            FieldPanel('stats_description'),
            FieldPanel('stats_customers_count'),
            FieldPanel('stats_customers_label'),
            FieldPanel('stats_products_count'),
            FieldPanel('stats_products_label'),
            FieldPanel('stats_years_experience'),
            FieldPanel('stats_years_label'),
            FieldPanel('stats_support_text'),
            FieldPanel('stats_support_label'),
        ], heading='Statistics'),
        MultiFieldPanel([
            FieldPanel('gallery_title_part1'),
            FieldPanel('gallery_title_part2'),
            FieldPanel('gallery_description'),
            FieldPanel('virtual_tour_url'),
            FieldPanel('virtual_tour_button_text'),
            InlinePanel('gallery_images', label="Gallery Images"),
        ], heading='Gallery Section'),
        MultiFieldPanel([
            FieldPanel('mission_vision_title_part1'),
            FieldPanel('mission_vision_title_part2'),
            FieldPanel('mission_title'),
            FieldPanel('mission_content'),
            FieldPanel('vision_title'),
            FieldPanel('vision_content'),
        ], heading='Mission & Vision'),
        MultiFieldPanel([
            FieldPanel('why_choose_title_part1'),
            FieldPanel('why_choose_title_part2'),
            FieldPanel('why_choose_description'),
            InlinePanel('why_choose_us_items', label="Why Choose Us Items"),
        ], heading='Why Choose Us Section'),
        MultiFieldPanel([
            FieldPanel('testimonials_title_part1'),
            FieldPanel('testimonials_title_part2'),
            FieldPanel('testimonials_description'),
            FieldPanel('testimonials_video_url'),
            InlinePanel('testimonials', label="Main Testimonials"),
            InlinePanel('customer_reviews', label="Customer Reviews"),
        ], heading='Testimonials Section'),
        MultiFieldPanel([
            FieldPanel('location_title'),
            FieldPanel('location_description'),
            FieldPanel('location_address_label'),
            FieldPanel('location_address'),
            FieldPanel('location_phone_label'),
            FieldPanel('location_phone1'),
            FieldPanel('location_phone2'),
            FieldPanel('location_email_label'),
            FieldPanel('location_email'),
            FieldPanel('location_hours_label'),
            FieldPanel('location_maps_url'),
        ], heading='Location & Contact'),
        MultiFieldPanel([
            FieldPanel('hours_monday_thursday'),
            FieldPanel('hours_saturday_sunday'),
            FieldPanel('hours_friday'),
        ], heading='Business Hours'),
        MultiFieldPanel([
            FieldPanel('cta_title'),
            FieldPanel('cta_description'),
            FieldPanel('cta_button1_text'),
            FieldPanel('cta_button1_url'),
            FieldPanel('cta_button2_text'),
            FieldPanel('cta_button2_url'),
        ], heading='Call to Action'),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_title_part1'),
        index.SearchField('story_content'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # This page no longer shows store data
        # Add any additional context variables here
        return context


# Contact Page
class ContactPage(CMSBasePage):
    """CMS Contact Page - manages the contact page content"""
    template = 'contact.html'
    
    # Page Header
    page_title_part1 = models.CharField(max_length=50, default="GET IN")
    page_title_part2 = models.CharField(max_length=50, default="TOUCH")
    page_description = models.TextField(default="Have questions? We'd love to hear from you.")
    
    # Contact Information
    contact_title = models.CharField(max_length=100, default="Contact Information")
    address_label = models.CharField(max_length=50, default="Address")
    address_text = models.TextField(default="Dubai Plaza, shop#13 basement, Bahawalpur, 63100")
    address_url = models.URLField(blank=True, help_text="Google Maps URL")
    
    phone_label = models.CharField(max_length=50, default="Phone")
    phone1 = models.CharField(max_length=20, default="+92 300 9681212")
    phone2 = models.CharField(max_length=20, default="+92 315 9682684")
    
    email_label = models.CharField(max_length=50, default="Email")
    email = models.EmailField(default="mobilercornerbwp@gmail.com")
    
    # Business Hours
    hours_title = models.CharField(max_length=100, default="Business Hours")
    hours_weekdays_label = models.CharField(max_length=50, default="Monday - Thursday")
    hours_weekdays_time = models.CharField(max_length=50, default="11:00 AM - 11:00 PM")
    hours_weekend_label = models.CharField(max_length=50, default="Saturday - Sunday")
    hours_weekend_time = models.CharField(max_length=50, default="12:00 PM - 11:00 PM")
    hours_friday_label = models.CharField(max_length=50, default="Friday")
    hours_friday_time = models.CharField(max_length=50, default="Closed")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('page_title_part1'),
            FieldPanel('page_title_part2'),
            FieldPanel('page_description'),
        ], heading='Page Header'),
        MultiFieldPanel([
            FieldPanel('contact_title'),
            FieldPanel('address_label'),
            FieldPanel('address_text'),
            FieldPanel('address_url'),
            FieldPanel('phone_label'),
            FieldPanel('phone1'),
            FieldPanel('phone2'),
            FieldPanel('email_label'),
            FieldPanel('email'),
        ], heading='Contact Information'),
        MultiFieldPanel([
            FieldPanel('hours_title'),
            FieldPanel('hours_weekdays_label'),
            FieldPanel('hours_weekdays_time'),
            FieldPanel('hours_weekend_label'),
            FieldPanel('hours_weekend_time'),
            FieldPanel('hours_friday_label'),
            FieldPanel('hours_friday_time'),
        ], heading='Business Hours'),
    ]