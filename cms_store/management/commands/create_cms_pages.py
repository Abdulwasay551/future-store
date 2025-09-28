from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from cms_store.models import (
    HomePage, StorePage, AboutPage, ContactPage, 
    CategoryPage, CompanyPage, ProductPage
)
from store.models import Category, Company, Product


class Command(BaseCommand):
    help = 'Create initial CMS pages'

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
            )
            root_page.add_child(instance=home_page)
            
            # Set as the site's root page
            site.root_page = home_page
            site.save()
            
            self.stdout.write(self.style.SUCCESS(f'Created home page: {home_page.title}'))

        # Create Store Page
        home_page = HomePage.objects.first()
        if home_page and not StorePage.objects.exists():
            store_page = StorePage(
                title='Store',
                slug='store',
                page_title='Our Products',
                page_subtitle='Discover our premium collection of mobile devices and accessories',
            )
            home_page.add_child(instance=store_page)
            self.stdout.write(self.style.SUCCESS(f'Created store page: {store_page.title}'))

        # Create About Page
        if home_page and not AboutPage.objects.exists():
            about_page = AboutPage(
                title='About Us',
                slug='about',
                hero_title_part1='ABOUT',
                hero_title_part2='MOBILE CORNER',
                hero_description='Your trusted partner in mobile technology since day one',
            )
            home_page.add_child(instance=about_page)
            self.stdout.write(self.style.SUCCESS(f'Created about page: {about_page.title}'))

        # Create Contact Page
        if home_page and not ContactPage.objects.exists():
            contact_page = ContactPage(
                title='Contact',
                slug='contact',
                page_title_part1='GET IN',
                page_title_part2='TOUCH',
                page_description="Have questions? We'd love to hear from you.",
            )
            home_page.add_child(instance=contact_page)
            self.stdout.write(self.style.SUCCESS(f'Created contact page: {contact_page.title}'))

        # Create Category Pages
        categories = Category.objects.all()
        for category in categories:
            if not CategoryPage.objects.filter(category=category).exists():
                category_page = CategoryPage(
                    title=category.name,
                    slug=f'categories-{category.slug}',
                    category=category,
                    introduction=f'<p>Explore {category.name} products from top brands.</p>',
                )
                home_page.add_child(instance=category_page)
                self.stdout.write(self.style.SUCCESS(f'Created category page: {category_page.title}'))

        # Create Company Pages
        companies = Company.objects.all()
        for company in companies:
            if not CompanyPage.objects.filter(company=company).exists():
                company_page = CompanyPage(
                    title=f'{company.name} - {company.category.name}',
                    slug=f'companies-{company.slug}',
                    company=company,
                    introduction=f'<p>Discover {company.name} products in our {company.category.name} category.</p>',
                )
                home_page.add_child(instance=company_page)
                self.stdout.write(self.style.SUCCESS(f'Created company page: {company_page.title}'))

        # Create Product Detail Pages for featured products
        store_page = StorePage.objects.first()
        if store_page:
            featured_products = Product.objects.filter(is_featured=True)[:10]  # Limit to first 10 featured products
            for product in featured_products:
                if not ProductPage.objects.filter(product=product).exists():
                    product_page = ProductPage(
                        title=product.name,
                        slug=f'product-{product.slug}',
                        product=product,
                        additional_description=f'<p>Learn more about {product.name} and its amazing features.</p>',
                    )
                    store_page.add_child(instance=product_page)
                    self.stdout.write(self.style.SUCCESS(f'Created product page: {product_page.title}'))

        self.stdout.write(self.style.SUCCESS('Initial CMS pages created successfully!'))