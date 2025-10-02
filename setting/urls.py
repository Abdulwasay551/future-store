"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request
from store.views import admin_dashboard

# Import Wagtail URLs
try:
    from wagtail.admin import urls as wagtailadmin_urls
    from wagtail import urls as wagtail_urls
    from wagtail.documents import urls as wagtaildocs_urls
    from wagtail.contrib.sitemaps.views import sitemap
    WAGTAIL_AVAILABLE = True
except ImportError:
    WAGTAIL_AVAILABLE = False

def debug_settings(request):
    """Debug view to check current settings"""
    return JsonResponse({
        'DEBUG': settings.DEBUG,
        'DEVELOPMENT': settings.DEVELOPMENT,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'SECURE_SSL_REDIRECT': settings.SECURE_SSL_REDIRECT,
        'SESSION_COOKIE_SECURE': settings.SESSION_COOKIE_SECURE,
        'CSRF_COOKIE_SECURE': settings.CSRF_COOKIE_SECURE,
        'HOST': request.get_host(),
        'HOST_IN_ALLOWED': request.get_host() in settings.ALLOWED_HOSTS,
        'WILDCARD_IN_ALLOWED': '*' in settings.ALLOWED_HOSTS,
    })

# Custom error handlers
def custom_404(request, exception=None):
    return page_not_found(request, exception, template_name='404.html')

def custom_500(request):
    return server_error(request, template_name='500.html')

def custom_403(request, exception=None):
    return permission_denied(request, exception, template_name='403.html')

def custom_400(request, exception=None):
    return bad_request(request, exception, template_name='400.html')

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),  # Django admin (Unfold)
    
    # Keep your existing user auth and store URLs working
    path('', include('user_auth.urls')),  # Keep user_auth at root for compatibility
    path('store/', include('store.urls')),  # Store URLs (both views and API)
    path('', include('cms_store.urls')),  # CMS/Blog URLs
    path('chatbot/', include('chatbot.urls')),  # Include chatbot app URLs
    path('erp/', include('inventory_erp.urls')),  # Include inventory_erp app URLs
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('debug/', debug_settings, name='debug_settings'),
]

# Add Wagtail URLs if available (admin only)
if WAGTAIL_AVAILABLE:
    urlpatterns += [
        path('cms-admin/', include(wagtailadmin_urls)),  # Wagtail CMS admin only
        path('documents/', include(wagtaildocs_urls)),  # Wagtail documents
        path('sitemap.xml', sitemap, name='sitemap'),  # Sitemap
    ]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)