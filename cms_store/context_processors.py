from cms_store.models import HomePage, AboutPage, ContactPage


def cms_context(request):
    """
    Context processor to make CMS content available in all templates
    """
    context = {}
    
    try:
        # Get the CMS pages
        home_page = HomePage.objects.live().first()
        about_page = AboutPage.objects.live().first()
        contact_page = ContactPage.objects.live().first()
        
        # Add CMS data to context
        if home_page:
            context['cms_home'] = home_page
            
        if about_page:
            context['cms_about'] = about_page
            
        if contact_page:
            context['cms_contact'] = contact_page
            
    except Exception:
        # If CMS pages don't exist or there's an error, return empty context
        pass
        
    return context