from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from social_django.utils import load_strategy
from social_core.exceptions import AuthAlreadyAssociated
from .models import User
from store.models import Contact, Order

def home(request):
    # Get featured products (newest and highest rated)
    from store.models import Product
    featured_products = Product.objects.filter(is_available=True).order_by('-created_at')[:3]
    return render(request, 'index.html', {'featured_products': featured_products})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'auth/signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/signup.html')

        try:
            # Validate password strength
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return render(request, 'auth/signup.html')

        user = User.objects.create_user(email=email, password=password1)
        login(request, user)
        return redirect('home')

    return render(request, 'auth/signup.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    addresses = request.user.addresses.all().order_by('-is_default')
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    return render(request, 'auth/profile.html', {
        'addresses': addresses,
        'recent_orders': recent_orders
    })

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 5)  # Show 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'auth/orders.html', {
        'orders': page_obj,
        'page_obj': page_obj
    })

def about_view(request):
    return render(request, 'about_us.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if all([name, email, subject, message]):
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields')
    
    return render(request, 'home_components/contact.html')

