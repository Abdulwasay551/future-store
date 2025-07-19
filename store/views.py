from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db import models
from .models import Category, Company, Product, Cart, CartItem, Review, Address, Order, OrderItem, ProductColor, Notification
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F, Count, Q, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta
import re

def test_view(request):
    """Simple test view to check if the app is working"""
    return HttpResponse("Store app is working!")

def product_list(request):
    # Get all categories
    categories = Category.objects.all()
    
    # Get selected category and company
    category_slug = request.GET.get('category')
    company_slug = request.GET.get('company')
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Start with all available products
    products = Product.objects.filter(is_available=True)
    
    # Apply search filter if provided
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(company__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
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
        'search_query': search_query,
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
    
    # Get selected color from query params
    selected_color_id = request.GET.get('color')
    selected_color = None
    if selected_color_id:
        selected_color = product.colors.filter(id=selected_color_id).first()
    
    # If no color selected, use primary color
    if not selected_color:
        selected_color = product.primary_color
    
    # Get images for selected color
    color_images = []
    if selected_color:
        color_images = selected_color.images.all()
    
    # If no color-specific images, fall back to product images
    if not color_images:
        color_images = product.images.all()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'selected_color': selected_color,
        'color_images': color_images,
    })

def get_color_images(request, product_id, color_id):
    """AJAX view to get images for a specific color"""
    product = get_object_or_404(Product, id=product_id)
    color = get_object_or_404(ProductColor, id=color_id, product=product)
    
    images = []
    for img in color.images.all():
        images.append({
            'id': img.id,
            'url': img.get_image_url,
            'alt_text': img.alt_text,
            'is_primary': img.is_primary
        })
    
    return JsonResponse({'images': images})

def get_product_colors(request, product_id):
    """AJAX view to get colors for a specific product"""
    product = get_object_or_404(Product, id=product_id)
    
    colors = []
    for color in product.colors.all():
        colors.append({
            'id': color.id,
            'name': color.name,
            'hex_code': color.hex_code,
            'stock': color.stock,
            'is_primary': color.is_primary
        })
    
    return JsonResponse({'colors': colors})

def test_colors(request):
    """Test view for debugging color functionality"""
    # Get the first product with colors for testing
    test_product = Product.objects.filter(colors__isnull=False).first()
    
    return render(request, 'store/test_colors.html', {
        'test_product': test_product,
    })

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get color from form data
    color_id = request.POST.get('color_id')
    color = None
    if color_id:
        color = product.colors.filter(id=color_id).first()
    
    # Try to get existing cart item with same product and color
    cart_item = None
    if color:
        cart_item = CartItem.objects.filter(cart=cart, product=product, color=color).first()
    else:
        cart_item = CartItem.objects.filter(cart=cart, product=product, color__isnull=True).first()
    
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, color=color, quantity=1)
    
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        # Validate required fields
        address_type = request.POST.get('address_type')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        
        if not all([address_type, street_address, city, state, postal_code]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('checkout')
        
        address = Address(
            user=request.user,
            address_type=address_type,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            is_default=request.POST.get('is_default') == 'on'
        )
        address.save()
        messages.success(request, 'Address added successfully.')
        return redirect('checkout')
    
    return redirect('checkout')

@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        print(f"Order placement attempt - User: {request.user.email}")
        
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart_detail')
        
        # Validate phone number
        phone_number = request.POST.get('phone_number', '').strip()
        if not phone_number:
            messages.error(request, 'Phone number is required for order placement.')
            return redirect('checkout')
        
        # Validate phone number format using regex
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(phone_number):
            messages.error(request, 'Please enter a valid phone number (e.g., +1234567890).')
            return redirect('checkout')
        
        address_id = request.POST.get('selected_address')
        print(f"Selected address ID: {address_id}")
        
        if not address_id:
            messages.error(request, 'Please select a delivery address.')
            return redirect('checkout')
        
        try:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            print(f"Address found: {address.street_address}")
        except Exception as e:
            print(f"Address error: {e}")
            messages.error(request, 'Invalid address selected.')
            return redirect('checkout')
        
        # Start transaction to ensure data consistency
        from django.db import transaction
        try:
            with transaction.atomic():
                print("Starting transaction...")
                
                # Update user's phone number if it's different
                if request.user.phone_number != phone_number:
                    request.user.phone_number = phone_number
                    request.user.save()
                    print(f"Updated user phone number to: {phone_number}")
                
                # Check stock availability and update stock
                for cart_item in cart.items.all():
                    print(f"Processing cart item: {cart_item.product.name} x {cart_item.quantity}")
                    
                    if cart_item.color:
                        # Check color-specific stock
                        if cart_item.color.stock < cart_item.quantity:
                            messages.error(
                                request,
                                f'Sorry, {cart_item.product.name} ({cart_item.color.name}) only has {cart_item.color.stock} items in stock.'
                            )
                            return redirect('cart_detail')
                    else:
                        # Check product total stock
                        if cart_item.product.total_stock < cart_item.quantity:
                            messages.error(
                                request,
                                f'Sorry, {cart_item.product.name} only has {cart_item.product.total_stock} items in stock.'
                            )
                            return redirect('cart_detail')
                    
                    # Reduce stock
                    if cart_item.color:
                        cart_item.color.stock -= cart_item.quantity
                        cart_item.color.save()
                        print(f"Reduced stock for {cart_item.color.name} to {cart_item.color.stock}")
                    else:
                        # Reduce from primary color if no specific color selected
                        primary_color = cart_item.product.primary_color
                        if primary_color and primary_color.stock >= cart_item.quantity:
                            primary_color.stock -= cart_item.quantity
                            primary_color.save()
                            print(f"Reduced stock for primary color to {primary_color.stock}")
                
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_amount=cart.total,
                    notes=request.POST.get('notes', ''),
                    payment_method='pending'  # Set to pending since payment will be discussed with representative
                )
                print(f"Order created with ID: {order.id}")
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        color=cart_item.color,
                        quantity=cart_item.quantity,
                        price=cart_item.product.discounted_price
                    )
                    print(f"Order item created: {cart_item.product.name}")
                
                # Clear the cart
                cart.items.all().delete()
                print("Cart cleared")
                
                # Create order notification
                try:
                    order.create_order_notification()
                    print("Order notification created")
                except Exception as e:
                    print(f"Notification error: {e}")
                    # Continue even if notification fails
                
                messages.success(request, 'Order placed successfully! Our representative will contact you shortly to discuss payment and delivery details.')
                print("Order placement successful!")
                return redirect('order_detail', order_id=order.id)
                
        except Exception as e:
            print(f"Order creation error: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, 'An error occurred while processing your order. Please try again.')
            return redirect('checkout')
    
    return redirect('checkout')

@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Mark order notifications as read
    order.notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'store/order_detail.html', {'order': order})

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required(login_url='login')
def get_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'store/review_item.html', {'review': review})

@login_required(login_url='login')
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

@login_required(login_url='login')
def notifications_list(request):
    """View user notifications"""
    notifications = request.user.notifications.all()[:50]  # Last 50 notifications
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    return render(request, 'store/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required(login_url='login')
def mark_notification_read(request, notification_id):
    """Mark a notification as read via AJAX"""
    from django.http import JsonResponse
    try:
        notification = request.user.notifications.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})

@login_required(login_url='login')
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    from django.http import JsonResponse
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True})
