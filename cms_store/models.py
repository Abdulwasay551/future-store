from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from store.models import Product, Category, Company
from django.core.paginator import Paginator
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey


# Base Page
class CMSBasePage(Page):
    """Base page class for CMS pages"""
    
    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        # Add categories for navigation
        context['categories'] = Category.objects.all()[:10]
        # Add featured products for home page
        context['featured_products'] = Product.objects.filter(is_featured=True, is_available=True)[:3]
        return context


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
        # Add data for the existing template
        context['featured_products'] = Product.objects.filter(is_featured=True)[:8]
        context['categories'] = Category.objects.all()[:6]
        context['companies'] = Company.objects.filter(is_featured=True)[:8]
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
    stats_customers_count = models.IntegerField(default=10000)
    stats_products_count = models.IntegerField(default=500)
    stats_years_experience = models.IntegerField(default=10)
    stats_brands_count = models.IntegerField(default=15)
    
    # Gallery Section
    gallery_title = models.CharField(max_length=100, default="Store Gallery")
    gallery_description = models.TextField(default="Take a look at our premium store and facilities")
    virtual_tour_url = models.URLField(blank=True, help_text="Virtual tour URL")
    
    # Mission & Vision
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_content = RichTextField(blank=True)
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_content = RichTextField(blank=True)
    
    # Why Choose Us Section
    why_choose_title = models.CharField(max_length=100, default="Why Choose Us")
    why_choose_description = models.TextField(default="Discover what makes us the preferred choice for mobile technology")
    
    # Testimonials Section
    testimonials_title = models.CharField(max_length=100, default="What Our Customers Say")
    testimonials_description = models.TextField(default="Real experiences from real customers")
    testimonials_video_url = models.URLField(blank=True, help_text="Customer testimonials video URL")
    
    # Location Section
    location_title = models.CharField(max_length=100, default="Visit Our Store")
    location_address = models.TextField(default="Dubai Plaza, shop#13 basement, Bahawalpur, 63100")
    location_phone1 = models.CharField(max_length=20, default="+92 300 9681212")
    location_phone2 = models.CharField(max_length=20, default="+92 315 9682684")
    location_email = models.EmailField(default="mobilercornerbwp@gmail.com")
    location_maps_url = models.URLField(blank=True, help_text="Google Maps URL")
    
    # Business Hours
    hours_monday_thursday = models.CharField(max_length=50, default="11:00 AM - 11:00 PM")
    hours_saturday_sunday = models.CharField(max_length=50, default="12:00 PM - 11:00 PM")
    hours_friday = models.CharField(max_length=50, default="Closed")
    
    # CTA Section
    cta_title = models.CharField(max_length=100, default="Ready to Get Started?")
    cta_description = models.TextField(default="Join thousands of satisfied customers who trust Mobile Corner")
    cta_button_text = models.CharField(max_length=50, default="Shop Now")
    cta_button_url = models.URLField(blank=True)
    
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
            FieldPanel('stats_customers_count'),
            FieldPanel('stats_products_count'),
            FieldPanel('stats_years_experience'),
            FieldPanel('stats_brands_count'),
        ], heading='Statistics'),
        MultiFieldPanel([
            FieldPanel('gallery_title'),
            FieldPanel('gallery_description'),
            FieldPanel('virtual_tour_url'),
            InlinePanel('gallery_images', label="Gallery Images"),
        ], heading='Gallery Section'),
        MultiFieldPanel([
            FieldPanel('mission_title'),
            FieldPanel('mission_content'),
            FieldPanel('vision_title'),
            FieldPanel('vision_content'),
        ], heading='Mission & Vision'),
        MultiFieldPanel([
            FieldPanel('why_choose_title'),
            FieldPanel('why_choose_description'),
            InlinePanel('why_choose_us_items', label="Why Choose Us Items"),
        ], heading='Why Choose Us Section'),
        MultiFieldPanel([
            FieldPanel('testimonials_title'),
            FieldPanel('testimonials_description'),
            FieldPanel('testimonials_video_url'),
            InlinePanel('testimonials', label="Testimonials"),
        ], heading='Testimonials Section'),
        MultiFieldPanel([
            FieldPanel('location_title'),
            FieldPanel('location_address'),
            FieldPanel('location_phone1'),
            FieldPanel('location_phone2'),
            FieldPanel('location_email'),
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
            FieldPanel('cta_button_text'),
            FieldPanel('cta_button_url'),
        ], heading='Call to Action'),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_title_part1'),
        index.SearchField('story_content'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Add data for the existing template
        context['companies'] = Company.objects.all()
        context['total_products'] = Product.objects.count()
        context['total_categories'] = Category.objects.count()
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


# Store Pages
class StorePage(CMSBasePage):
    """CMS Store Page - main store listing page"""
    template = 'store/product_list.html'  # Use existing template
    
    # Page Header
    page_title = models.CharField(max_length=100, default="Our Products")
    page_subtitle = models.TextField(default="Discover our premium collection of mobile devices and accessories")
    page_banner_url = models.URLField(blank=True, help_text="Page banner image URL")
    
    # Filter Options
    show_categories = models.BooleanField(default=True, help_text="Show category filter")
    show_companies = models.BooleanField(default=True, help_text="Show brand filter")
    show_price_filter = models.BooleanField(default=True, help_text="Show price filter")
    show_search = models.BooleanField(default=True, help_text="Show search functionality")
    
    # Display Options
    products_per_page = models.IntegerField(default=12, help_text="Number of products per page")
    show_product_badges = models.BooleanField(default=True, help_text="Show featured/new badges")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('page_title'),
            FieldPanel('page_subtitle'),
            FieldPanel('page_banner_url'),
        ], heading='Page Header'),
        MultiFieldPanel([
            FieldPanel('show_categories'),
            FieldPanel('show_companies'),
            FieldPanel('show_price_filter'),
            FieldPanel('show_search'),
        ], heading='Filter Options'),
        MultiFieldPanel([
            FieldPanel('products_per_page'),
            FieldPanel('show_product_badges'),
        ], heading='Display Options'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get query parameters for filtering
        category_id = request.GET.get('category')
        company_id = request.GET.get('company')
        search_query = request.GET.get('search')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        # Start with all products
        products = Product.objects.filter(is_available=True)
        
        # Apply filters
        if category_id:
            products = products.filter(category_id=category_id)
        if company_id:
            products = products.filter(company_id=company_id)
        if search_query:
            products = products.filter(
                models.Q(name__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
        if min_price:
            products = products.filter(selling_price__gte=min_price)
        if max_price:
            products = products.filter(selling_price__lte=max_price)
        
        # Pagination
        from django.core.paginator import Paginator
        paginator = Paginator(products, self.products_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'products': page_obj.object_list,
            'page_obj': page_obj,
            'categories': Category.objects.all() if self.show_categories else None,
            'companies': Company.objects.all() if self.show_companies else None,
            'current_category': category_id,
            'current_company': company_id,
            'search_query': search_query,
            'min_price': min_price,
            'max_price': max_price,
        })
        return context


# Product Detail Page
class ProductPage(CMSBasePage):
    """CMS Product Detail Page - individual product pages"""
    template = 'store/product_detail.html'  # Use existing template
    
    # Related product to display
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.PROTECT,
        related_name='cms_pages'
    )
    
    # SEO and Display Options
    show_related_products = models.BooleanField(default=True)
    show_specifications = models.BooleanField(default=True)
    show_reviews = models.BooleanField(default=True)
    show_company_products = models.BooleanField(default=True)
    
    # Custom Content
    additional_description = RichTextField(blank=True, help_text="Additional product description")
    warranty_info = models.TextField(blank=True, help_text="Warranty information")
    delivery_info = models.TextField(blank=True, help_text="Delivery information")
    
    content_panels = Page.content_panels + [
        FieldPanel('product'),
        MultiFieldPanel([
            FieldPanel('show_related_products'),
            FieldPanel('show_specifications'),
            FieldPanel('show_reviews'),
            FieldPanel('show_company_products'),
        ], heading='Display Options'),
        MultiFieldPanel([
            FieldPanel('additional_description'),
            FieldPanel('warranty_info'),
            FieldPanel('delivery_info'),
        ], heading='Additional Information'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['product'] = self.product
        
        if self.show_related_products:
            context['related_products'] = Product.objects.filter(
                category=self.product.category
            ).exclude(id=self.product.id)[:4]
            
        if self.show_company_products:
            context['company_products'] = Product.objects.filter(
                company=self.product.company
            ).exclude(id=self.product.id)[:4]
            
        return context
    
    def save(self, *args, **kwargs):
        # Auto-set title and slug from product
        if self.product:
            self.title = self.product.name
            self.slug = self.product.slug
        super().save(*args, **kwargs)


# Category Page
class CategoryPage(CMSBasePage):
    """CMS Category Page"""
    template = 'store/category_products.html'  # Use existing template
    
    # Link to the actual category
    category = models.ForeignKey(
        'store.Category',
        on_delete=models.PROTECT,
        related_name='cms_pages'
    )
    
    introduction = RichTextField(blank=True)
    products_per_page = models.IntegerField(default=12)
    
    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('introduction'),
        FieldPanel('products_per_page'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get products for this category
        products = Product.objects.filter(
            category=self.category,
            is_available=True
        )
        
        # Filter by company if provided
        company_slug = request.GET.get('company')
        if company_slug:
            try:
                company = Company.objects.get(slug=company_slug)
                products = products.filter(company=company)
                context['current_company'] = company
            except Company.DoesNotExist:
                pass
        
        # Pagination
        paginator = Paginator(products, self.products_per_page)
        page = request.GET.get('page')
        products_page = paginator.get_page(page)
        
        context['category'] = self.category
        context['products'] = products_page
        context['companies'] = Company.objects.filter(
            category=self.category
        ).distinct()
        return context
    
    def save(self, *args, **kwargs):
        # Auto-set title and slug from category
        if self.category:
            self.title = self.category.name
            self.slug = self.category.slug
        super().save(*args, **kwargs)


# Company Page
class CompanyPage(CMSBasePage):
    """CMS Company Page"""
    template = 'store/company_products.html'  # Use existing template
    
    # Link to the actual company
    company = models.ForeignKey(
        'store.Company',
        on_delete=models.PROTECT,
        related_name='cms_pages'
    )
    
    introduction = RichTextField(blank=True)
    products_per_page = models.IntegerField(default=12)
    
    content_panels = Page.content_panels + [
        FieldPanel('company'),
        FieldPanel('introduction'),
        FieldPanel('products_per_page'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get products for this company
        products = Product.objects.filter(
            company=self.company,
            is_available=True
        )
        
        # Pagination
        paginator = Paginator(products, self.products_per_page)
        page = request.GET.get('page')
        products_page = paginator.get_page(page)
        
        context['company'] = self.company
        context['products'] = products_page
        return context
    
    def save(self, *args, **kwargs):
        # Auto-set title and slug from company
        if self.company:
            self.title = f"{self.company.name} - {self.company.category.name}"
            self.slug = f"{self.company.slug}-{self.company.category.slug}"
        super().save(*args, **kwargs)


# General Content Page
class ContentPage(CMSBasePage):
    """General CMS Content Page"""
    template = 'cms_store/content_page.html'
    
    introduction = RichTextField(blank=True)
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('body'),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]