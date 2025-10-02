from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from cms_store.models import BlogIndexPage, BlogPost, BlogCategory, BlogTag


def blog_index(request):
    """Blog index view with filtering and pagination"""
    try:
        # Get the blog index page from Wagtail
        blog_page = BlogIndexPage.objects.live().first()
        if not blog_page:
            # Fallback context if no blog page exists
            context = {
                'page': None,
                'posts': BlogPost.objects.none(),
                'featured_posts': BlogPost.objects.none(),
                'categories': BlogCategory.objects.all()[:6],
                'recent_posts': BlogPost.objects.none(),
            }
            return render(request, 'blog/blog_index_page.html', context)
        
        # Get all live blog posts
        posts = BlogPost.objects.live().order_by('-publish_date')
        
        # Filter by category if specified
        category_slug = request.GET.get('category')
        if category_slug:
            posts = posts.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = request.GET.get('search')
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(body__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(posts, 9)  # 9 posts per page
        page_number = request.GET.get('page')
        posts_page = paginator.get_page(page_number)
        
        # Get featured posts (first 2 featured posts)
        featured_posts = BlogPost.objects.live().filter(is_featured=True)[:2]
        
        # Get categories for the filter
        categories = BlogCategory.objects.all()[:6]
        
        # Get recent posts for sidebar
        recent_posts = BlogPost.objects.live().order_by('-publish_date')[:5]
        
        context = {
            'page': blog_page,
            'posts': posts_page,
            'featured_posts': featured_posts,
            'categories': categories,
            'recent_posts': recent_posts,
            'current_category': category_slug,
            'search_query': search_query,
        }
        
        return render(request, 'blog/blog_index_page.html', context)
        
    except Exception as e:
        # Fallback context in case of any error
        context = {
            'page': None,
            'posts': BlogPost.objects.none(),
            'featured_posts': BlogPost.objects.none(),
            'categories': BlogCategory.objects.all()[:6],
            'recent_posts': BlogPost.objects.none(),
            'error': str(e)
        }
        return render(request, 'blog/blog_index_page.html', context)


def blog_post_detail(request, slug):
    """Individual blog post view"""
    try:
        # Get the blog post
        post = get_object_or_404(BlogPost, slug=slug)
        
        # Get related posts (same category, excluding current post)
        related_posts = BlogPost.objects.live().filter(
            category=post.category
        ).exclude(id=post.id).order_by('-publish_date')[:4]
        
        # If not enough related posts from same category, get recent posts
        if related_posts.count() < 4:
            additional_posts = BlogPost.objects.live().exclude(
                id=post.id
            ).exclude(
                id__in=[p.id for p in related_posts]
            ).order_by('-publish_date')[:4-related_posts.count()]
            related_posts = list(related_posts) + list(additional_posts)
        
        # Get recent posts for sidebar
        recent_posts = BlogPost.objects.live().exclude(id=post.id).order_by('-publish_date')[:5]
        
        # Get all categories for sidebar
        categories = BlogCategory.objects.all()
        
        context = {
            'self': post,  # Use 'self' to match Wagtail template expectations
            'page': post,
            'related_posts': related_posts,
            'recent_posts': recent_posts,
            'categories': categories,
        }
        
        return render(request, 'blog/blog_page.html', context)
        
    except BlogPost.DoesNotExist:
        # Fallback to blog index if post not found
        return blog_index(request)


def blog_category(request, slug):
    """Blog category view"""
    category = get_object_or_404(BlogCategory, slug=slug)
    
    # Get posts in this category
    posts = BlogPost.objects.live().filter(category=category).order_by('-publish_date')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    # Get blog index page for context
    blog_page = BlogIndexPage.objects.live().first()
    
    # Get all categories for the filter
    categories = BlogCategory.objects.all()
    
    context = {
        'page': blog_page,
        'posts': posts_page,
        'categories': categories,
        'current_category': category,
        'category': category,
    }
    
    return render(request, 'blog/blog_index_page.html', context)


def blog_tag(request, slug):
    """Blog tag view"""
    tag = get_object_or_404(BlogTag, slug=slug)
    
    # Get posts with this tag
    posts = BlogPost.objects.live().filter(tags=tag).order_by('-publish_date')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    # Get blog index page for context
    blog_page = BlogIndexPage.objects.live().first()
    
    # Get all categories for the filter
    categories = BlogCategory.objects.all()
    
    context = {
        'page': blog_page,
        'posts': posts_page,
        'categories': categories,
        'current_tag': tag,
        'tag': tag,
    }
    
    return render(request, 'blog/blog_index_page.html', context)