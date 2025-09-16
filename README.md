# Future Store - Mobile Business E-Commerce Platform

A modern Django-based e-commerce platform built specifically for mobile device retail business. Features a futuristic design with dark/light mode themes, component-based rendering, and comprehensive inventory management. Perfect for mobile stores and electronics retailers.

## 🌟 Key Features

### 📱 Mobile-Focused E-Commerce
- **Mobile Device Catalog**: Specialized for smartphones, tablets, and accessories
- **Color Variants**: Product variants with color-specific images and stock
- **Smart Shopping Cart**: HTMX-powered cart with instant updates
- **Order Processing**: Complete order management workflow
- **Customer Reviews**: Product rating and feedback system
- **Responsive Design**: Mobile-first design optimized for all devices

### 🎨 Modern UI/UX with Tailwind CSS
- **Futuristic Design**: Clean, modern interface with tech-inspired aesthetics
- **Dark/Light Mode**: Toggle between themes with smooth transitions
- **Component-Based**: HTMX for React-like component rendering with minimal page loads
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **Smooth Animations**: Tailwind-powered animations and transitions
- **Mobile-Optimized**: Touch-friendly interface for mobile users

### 🤖 AI-Powered Customer Support
- **Smart Chatbot**: AI-driven customer assistance using Ollama
- **Product Recommendations**: Personalized device suggestions
- **Session Management**: Persistent chat sessions for customers
- **Interactive Help**: Guided product selection assistance

### 📦 Complete Inventory & Business Management
- **Device Inventory**: Comprehensive mobile device and accessory management
- **SKU Generation**: Automatic product identification and tracking
- **Dealer Network**: Multi-tier dealer management (Main/Sub/Second-hand dealers)
- **Purchase Orders**: Complete supplier and purchase workflow
- **Sales Management**: Retail and wholesale sales processing
- **Payment Tracking**: Multiple payment method support
- **Stock Control**: Real-time inventory with IMEI/Serial number tracking

### 👤 User Authentication & Management
- **Email-Based Auth**: Modern authentication without usernames
- **Social Login**: Google OAuth2 integration
- **Customer Profiles**: Complete user profile management
- **Address Management**: Multiple shipping addresses
- **Role-Based Access**: Admin, staff, and customer role separation

### ⚡ Performance & Technology
- **HTMX Integration**: Component-based rendering for faster page loads
- **Minimal JavaScript**: Lightweight frontend with HTMX and Alpine.js
- **Django Unfold**: Beautiful, customized admin interface
- **Optimized Loading**: Fast page transitions and minimal reload times

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js (for Tailwind CSS, optional)
- Git

### Basic Django Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abdulwasay551/future-store.git
   cd future-store
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup** (Minimal required)
   Create a `.env` file in the root directory:
   ```bash
   # Basic Configuration
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=True
   DEVELOPMENT=True
   
   # Google OAuth2 (optional for social login)
   GOOGLE_OAUTH2_KEY=your-google-oauth2-key
   GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret
   ```

5. **Database Setup** (Uses SQLite by default)
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load Sample Mobile Data** (Optional)
   ```bash
   python manage.py populate_store
   python manage.py populate_sample_data
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` to see your mobile store!

### Quick Setup Notes
- **No complex setup required** - Uses SQLite database by default
- **Tailwind CSS** - Pre-configured and included via CDN
- **HTMX** - Already integrated for component-based interactions
- **Dark/Light mode** - Works out of the box
- **Admin panel** - Access at `/admin/` with custom Unfold theme

## 🛠 Technology Stack

### Backend
- **Django 5.2+** - Python web framework
- **Django Unfold** - Modern admin interface
- **SQLite** - Default database (PostgreSQL supported)
- **Django Social Auth** - Google OAuth2 integration
- **Ollama** - AI chatbot integration

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **HTMX** - Modern HTML-driven interactions
- **Alpine.js** - Lightweight JavaScript framework
- **Font Awesome** - Icon library
- **CSS Custom Properties** - Dynamic theming support

### Features
- **Dark/Light Mode** - Automatic theme switching
- **Component-Based** - HTMX for React-like experience
- **Responsive Design** - Mobile-first approach
- **Real-time Updates** - HTMX-powered dynamic content
- **Modern UI** - Futuristic design with smooth animations

## 📁 Project Structure

```
future-store/
├── setting/                 # Django project configuration
│   ├── settings.py         # Main settings with theme support
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── store/                  # Main e-commerce app
│   ├── models.py          # Product, Cart, Order models
│   ├── views.py           # Store views with HTMX support
│   ├── templates/         # HTMX-powered templates
│   └── management/        # Sample data commands
├── user_auth/             # Authentication system
│   ├── models.py          # Custom User model
│   ├── views.py           # Auth views
│   └── templates/         # Auth templates with themes
├── chatbot/               # AI customer support
│   ├── models.py          # Chat session models
│   ├── views.py           # Ollama AI integration
│   └── ollama.py          # AI response generation
├── inventory_erp/         # Business management
│   ├── models.py          # Inventory and sales models
│   ├── views.py           # ERP functionality
│   └── templates/         # Business management UI
├── static/                # Static assets
│   ├── css/               # Tailwind and custom styles
│   ├── js/                # HTMX, Alpine.js, theme toggle
│   └── images/            # Mobile device images
├── requirements.txt       # Python dependencies
└── manage.py             # Django management
```

## 🎨 Themes & UI Features

### Dark/Light Mode
The application features a sophisticated theme system:

```javascript
// Toggle between themes
document.documentElement.classList.toggle('dark');

// Themes are persisted in localStorage
localStorage.theme = 'dark'; // or 'light'
```

### Tailwind CSS Configuration
Custom color scheme with CSS variables:
```css
:root {
  --mc-black: #000000;
  --mc-dark: #1a1a1a;
  --mc-accent: #d4af37;
  --mc-white: #ffffff;
}

.dark {
  /* Dark mode variants */
}
```

### HTMX Component System
React-like component behavior without JavaScript frameworks:
```html
<!-- Auto-updating cart -->
<div hx-get="/store/cart-count/" 
     hx-trigger="cart-updated from:body"
     hx-target="#cart-count">
  <!-- Cart count updates automatically -->
</div>
```

## 🏪 Business Features

### Mobile Store Management
Perfect for mobile device retailers:
- **Brand Management**: Apple, Samsung, Huawei, OnePlus, Oppo, Vivo, Xiaomi
- **Device Categories**: Smartphones, tablets, accessories
- **Color Variants**: Specific colors with individual inventory
- **IMEI Tracking**: Complete device identification
- **Dealer Network**: Wholesale and retail management

### Inventory System
- **Real-time Stock**: HTMX-powered inventory updates
- **Purchase Orders**: Supplier management and tracking
- **Sales Processing**: Retail and wholesale transactions
- **Payment Methods**: Cash, card, bank transfer, UPI support

### Customer Experience
- **Fast Loading**: HTMX eliminates page refreshes
- **Mobile Optimized**: Touch-friendly interface
- **Search & Filter**: Advanced product filtering
- **Wishlist**: Save favorite devices
- **Reviews**: Customer feedback system

## 🔧 Configuration & Setup

### Basic Django Settings
The application uses sensible defaults for quick setup:

```python
# settings.py - Key configurations
INSTALLED_APPS = [
    'unfold',  # Modern admin interface
    'django.contrib.admin',
    'social_django',  # Google OAuth2
    'user_auth',
    'store.apps.StoreConfig',
    'chatbot.apps.ChatbotConfig',
    'inventory_erp.apps.InventoryErpConfig',
]

# Database - SQLite by default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Theme Configuration
Automatic dark/light mode with system preference detection:
```javascript
// Auto-detect system theme preference
if (localStorage.theme === 'dark' || 
    (!('theme' in localStorage) && 
     window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
}
```

### HTMX Setup
Pre-configured for component-based interactions:
```html
<!-- Included in base template -->
<script src="{% static 'js/htmx.js' %}"></script>
<script src="{% static 'js/alpine.min.js' %}" defer></script>
```

### Social Authentication
Simple Google OAuth2 setup:
```python
# Add to .env file
GOOGLE_OAUTH2_KEY=your-client-id
GOOGLE_OAUTH2_SECRET=your-client-secret

# URLs automatically configured
path('social-auth/', include('social_django.urls')),
```

## 🚀 Deployment

### Vercel Deployment
The application is configured for Vercel deployment:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

3. **Environment Variables**
   Set the following in Vercel dashboard:
   - `DJANGO_SECRET_KEY`
   - `DEBUG=False`
   - `DEVELOPMENT=False`
   - Database credentials (if using external DB)
   - Google OAuth2 credentials

### Manual Deployment
For traditional hosting:

1. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

2. **Configure Web Server**
   Use Gunicorn with nginx:
   ```bash
   gunicorn setting.wsgi:application
   ```

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test store
python manage.py test user_auth
python manage.py test chatbot
python manage.py test inventory_erp

# Run specific test files
python manage.py test store.tests.test_models
```

### Test Coverage
The project includes comprehensive tests for:
- Model functionality and validation
- View responses and permissions
- Form validation
- API endpoints
- Authentication flows

## 📊 Admin Interface

Access the beautiful Django Unfold admin interface at `/admin/`

**Custom Admin Features:**
- **Modern Design**: Clean, futuristic interface
- **Dark/Light Mode**: Matches frontend theme
- **Mobile Management**: Easy product catalog management  
- **Order Processing**: Streamlined order workflow
- **Customer Management**: User accounts and profiles
- **Inventory Control**: Stock management and tracking
- **Sales Analytics**: Basic reporting dashboard

### Admin Customization
```python
# Custom Unfold configuration
UNFOLD = {
    "SITE_TITLE": "Mobile Corner Admin",
    "SITE_HEADER": "Mobile Store Management",
    "COLORS": {
        "primary": {
            "50": "#f0f9ff",
            "500": "#3b82f6",
            "600": "#2563eb",
        },
    },
}
```

## 🔗 API Endpoints

### Store API
- `GET /store/` - Mobile device listing with filters
- `GET /store/product/<slug>/` - Device details
- `POST /store/add-to-cart/<id>/` - Add to cart (HTMX)
- `GET /store/api/product/<id>/colors/` - Available colors
- `GET /store/api/product/<id>/color/<id>/images/` - Color images

### HTMX Endpoints
- `GET /store/cart-count/` - Dynamic cart count
- `POST /store/update-cart/` - Cart updates
- `GET /store/product-search/` - Live search results

### User API
- `POST /login/` - User authentication
- `POST /signup/` - User registration
- `GET /profile/` - User profile management
- `GET /orders/` - Order history

### Chatbot API
- `GET /chatbot/widget/` - Chat widget component
- `POST /chatbot/message/` - AI chat responses

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Ensure migrations are included
- Test deployment locally

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Documentation

For support and questions:
- **Issues**: [GitHub Issues](https://github.com/Abdulwasay551/future-store/issues)
- **Deployment**: See `DEPLOYMENT_GUIDE.md` for production setup
- **Business**: Perfect for mobile retail stores and electronics shops

## 🚦 Project Status

- ✅ **Mobile E-commerce**: Fully functional store
- ✅ **Tailwind CSS**: Complete styling system
- ✅ **HTMX Integration**: Component-based interactions
- ✅ **Dark/Light Themes**: Automatic theme switching  
- ✅ **Django Unfold**: Custom admin interface
- ✅ **User Authentication**: Complete auth system
- ✅ **Inventory ERP**: Business management features
- ✅ **AI Chatbot**: Customer support system
- ✅ **Deployment Ready**: Vercel and manual deployment support
- 🔄 **Mobile Apps**: Future native app development
- 🔄 **Payment Gateway**: Integration with local payment systems

---

**Built with ❤️ for mobile retail business using Django + Tailwind CSS + HTMX**

*Perfect for electronics stores, mobile shops, and device retailers looking for a modern, efficient e-commerce solution.*