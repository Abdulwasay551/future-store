from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()


@register.inclusion_tag('cms_store/seo_meta_tags.html', takes_context=True)
def seo_meta_tags(context):
    """Render SEO meta tags for the current page"""
    request = context['request']
    page = context.get('page')
    
    if not page:
        return {}
    
    # Get the canonical URL
    canonical_url = page.get_canonical_url() if hasattr(page, 'get_canonical_url') else page.get_full_url(request)
    
    return {
        'page': page,
        'request': request,
        'canonical_url': canonical_url,
    }


@register.simple_tag(takes_context=True)
def google_analytics(context):
    """Render Google Analytics code if GA ID is set"""
    page = context.get('page')
    if not page or not hasattr(page, 'google_analytics_id') or not page.google_analytics_id:
        return ''
    
    ga_code = f'''
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={page.google_analytics_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{page.google_analytics_id}');
    </script>
    '''
    return mark_safe(ga_code)


@register.simple_tag(takes_context=True)
def facebook_pixel(context):
    """Render Facebook Pixel code if Pixel ID is set"""
    page = context.get('page')
    if not page or not hasattr(page, 'facebook_pixel_id') or not page.facebook_pixel_id:
        return ''
    
    pixel_code = f'''
    <!-- Facebook Pixel -->
    <script>
        !function(f,b,e,v,n,t,s)
        {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '{page.facebook_pixel_id}');
        fbq('track', 'PageView');
    </script>
    <noscript>
        <img height="1" width="1" style="display:none"
             src="https://www.facebook.com/tr?id={page.facebook_pixel_id}&ev=PageView&noscript=1"/>
    </noscript>
    '''
    return mark_safe(pixel_code)


@register.simple_tag(takes_context=True)
def structured_data(context):
    """Generate JSON-LD structured data for SEO"""
    page = context.get('page')
    request = context.get('request')
    
    if not page:
        return ''
    
    # Basic organization data
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Mobile Corner",
        "url": request.build_absolute_uri('/'),
        "sameAs": [
            "https://www.facebook.com/mobilecorner",
            "https://www.instagram.com/mobilecorner",
            "https://twitter.com/mobilecorner"
        ]
    }
    
    # Add page-specific data
    if hasattr(page, 'get_meta_title'):
        data["@type"] = "WebPage"
        data["name"] = page.get_meta_title()
        data["description"] = page.get_meta_description()
        data["url"] = page.get_full_url(request)
    
    import json
    json_ld = f'<script type="application/ld+json">{json.dumps(data)}</script>'
    return mark_safe(json_ld)