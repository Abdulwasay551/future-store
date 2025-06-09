from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db import models
from .models import Category, Company, Product, Cart, CartItem, Review, Address, Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F, Count, Q, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta

def product_list(request):
    # Get all categories
    categories = Category.objects.all()
    
    # Get selected category and company
    category_slug = request.GET.get('category')
    company_slug = request.GET.get('company')
    
    # Start with all available products
    products = Product.objects.filter(is_available=True)
    
    # Filter by category and company if provided
    selected_category = None
    selected_company = None
    
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
        
        if company_slug:
            selected_company = get_object_or_404(Company, slug=company_slug, category=selected_category)
            products = products.filter(company=selected_company)
    
    # Apply price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Apply rating filter
    rating = request.GET.get('rating')
    if rating:
        products = products.annotate(
            avg_rating=models.Avg('reviews__rating')
        ).filter(avg_rating__gte=rating)
    
    # Apply availability filter
    availability = request.GET.get('availability')
    if availability == 'in_stock':
        products = products.filter(stock__gt=0)
    elif availability == 'out_of_stock':
        products = products.filter(stock=0)
    
    # Apply sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.annotate(
            avg_rating=models.Avg('reviews__rating')
        ).order_by('-avg_rating')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'selected_company': selected_company,
    }
    
    # If it's an HTMX request for just the products section
    if request.headers.get('HX-Target') == 'products-section':
        return render(request, 'store/products_section.html', context)
    
    # If it's an HTMX request for the full content
    if request.headers.get('HX-Request'):
        return render(request, 'store/product_list.html', context)
        
    # If it's a regular request
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.all().order_by('-created_at')
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews
    })

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Return only the cart count for HTMX request
    return render(request, 'store/cart_count.html', {'cart': cart})

@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required(login_url='login')
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
            return redirect('cart_detail')
    
    cart_item.save()
    return redirect('cart_detail')

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Update or create the review
        review, created = Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        messages.success(request, 'Your review has been submitted.')
        return redirect('product_detail', slug=product.slug)
    
    return redirect('product_list')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_detail')
    
    # Get all addresses for the user
    addresses = Address.objects.filter(user=request.user).order_by('-is_default')
    
    # Calculate cart total
    cart_total = cart.total
    
    context = {
        'cart': cart,
        'addresses': addresses,
        'cart_total': cart_total,
    }
    
    return render(request, 'store/checkout.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        address = Address(
            user=request.user,
            address_type=request.POST.get('address_type'),
            street_address=request.POST.get('street_address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            is_default=request.POST.get('is_default') == 'on'
        )
        address.save()
        messages.success(request, 'Address added successfully.')
        return redirect('checkout')
    
    return redirect('checkout')

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart_detail')
        
        address_id = request.POST.get('selected_address')
        if not address_id:
            messages.error(request, 'Please select a delivery address.')
            return redirect('checkout')
        
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        # Start transaction to ensure data consistency
        from django.db import transaction
        try:
            with transaction.atomic():
                # Check stock availability and update stock
                for cart_item in cart.items.all():
                    if cart_item.product.stock < cart_item.quantity:
                        messages.error(
                            request,
                            f'Sorry, {cart_item.product.name} only has {cart_item.product.stock} items in stock.'
                        )
                        return redirect('cart_detail')
                    
                    # Reduce stock
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()
                
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_amount=cart.total
                )
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                
                # Clear the cart
                cart.items.all().delete()
                
                messages.success(request, 'Order placed successfully!')
                return redirect('order_detail', order_id=order.id)
                
        except Exception as e:
            messages.error(request, 'An error occurred while processing your order. Please try again.')
            return redirect('checkout')
    
    return redirect('checkout')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def get_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'store/review_item.html', {'review': review})

@login_required
def load_more_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    page = int(request.GET.get('page', 1))
    reviews = product.reviews.all().order_by('-created_at')
    
    paginator = Paginator(reviews, 5)  # 5 reviews per page
    try:
        reviews_page = paginator.page(page)
    except:
        return HttpResponse('')  # Return empty if page is invalid
    
    context = {'reviews': reviews_page}
    if reviews_page.has_next():
        context['next_page'] = reviews_page.next_page_number()
    
    html = render_to_string('store/review_list.html', context)
    return HttpResponse(html)
