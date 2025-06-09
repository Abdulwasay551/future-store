from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import HttpResponse

def home(request):
    # Get featured products (newest and highest rated)
    from store.models import Product
    featured_products = Product.objects.filter(is_available=True).order_by('-created_at')[:3]
    return render(request, 'index.html', {'featured_products': featured_products})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'auth/login.html')
    
    return render(request, 'auth/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/signup.html')
        
        user = User.objects.create_user(email=email, password=password1)
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    
    return render(request, 'auth/signup.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')

@login_required
def profile_view(request):
    addresses = request.user.addresses.all().order_by('-is_default')
    recent_orders = request.user.orders.all().order_by('-created_at')[:3]
    
    return render(request, 'auth/profile.html', {
        'addresses': addresses,
        'recent_orders': recent_orders
    })

@login_required
def orders_view(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'auth/orders.html', {
        'orders': orders
    })

def about_view(request):
    return render(request, 'about_us.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you could add code to send email, save to database, etc.
        
        return HttpResponse(
            '<div class="p-4 bg-green-100 text-green-800 rounded-lg">'
            'Thank you for your message! We will get back to you soon.'
            '</div>'
        )
    
    return render(request, 'home_components/contact.html')