# Future Store - Django E-Commerce Platform

A comprehensive Django-based e-commerce platform with advanced features including inventory management, AI-powered chatbot, and multi-vendor support. Built with modern web technologies for mobile device retail and distribution.

## 🌟 Features

### 🛒 E-Commerce Store
- **Product Catalog**: Multi-category product listings with advanced filtering
- **Color Management**: Product variants with color-specific images and inventory
- **Shopping Cart**: Dynamic cart with real-time updates
- **Order Management**: Complete order processing workflow
- **User Reviews**: Product rating and review system
- **Responsive Design**: Mobile-first responsive design

### 🤖 AI-Powered Chatbot
- **Smart Recommendations**: AI-driven product recommendations using Ollama
- **User Preferences**: Personalized shopping assistance
- **Session Management**: Persistent chat sessions for users
- **Product Guidance**: Interactive product selection help

### 📦 Inventory ERP System
- **Device Management**: Comprehensive device catalog with SKU generation
- **Dealer Network**: Multi-tier dealer management (Main/Sub/Second-hand)
- **Purchase Orders**: Complete purchase workflow with tracking
- **Sales Management**: Retail and wholesale sales processing
- **Payment Tracking**: Multi-method payment recording
- **Stock Control**: Real-time inventory tracking with IMEI/Serial numbers

### 👥 User Management
- **Custom User Model**: Email-based authentication
- **Social Authentication**: Google OAuth2 integration
- **Profile Management**: User profiles with address management
- **Role-based Access**: Admin and user role separation

### 🎨 Modern UI/UX
- **Django Unfold**: Modern admin interface
- **Responsive Design**: Mobile-optimized interface
- **Dynamic Loading**: AJAX-powered interactions
- **Image Management**: Multiple image support with URL fallbacks

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL (optional, SQLite default)
- Git

### Installation

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

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```bash
   # Basic Configuration
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=True
   DEVELOPMENT=True
   
   # Google OAuth2 (optional)
   GOOGLE_OAUTH2_KEY=your-google-oauth2-key
   GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret
   
   # Database (optional - defaults to SQLite)
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=future_store
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email Configuration (optional)
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load Sample Data (Optional)**
   ```bash
   python manage.py populate_store
   python manage.py populate_sample_data
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` to see the application.

## 📁 Project Structure

```
future-store/
├── setting/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── store/                  # Main e-commerce app
│   ├── models.py          # Product, Cart, Order models
│   ├── views.py           # Store views and logic
│   ├── templates/         # Store templates
│   └── management/        # Custom management commands
├── user_auth/             # User authentication app
│   ├── models.py          # Custom User model
│   ├── views.py           # Auth views
│   └── templates/         # Auth templates
├── chatbot/               # AI chatbot app
│   ├── models.py          # Chat session models
│   ├── views.py           # Chatbot logic
│   └── ollama.py          # AI integration
├── inventory_erp/         # Inventory management app
│   ├── models.py          # ERP models
│   ├── views.py           # ERP views
│   └── templates/         # ERP templates
├── static/                # Static files (CSS, JS, images)
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## 🛠 Core Applications

### Store App
The main e-commerce functionality including:
- **Categories & Companies**: Hierarchical product organization
- **Products**: With color variants, pricing, and inventory
- **Shopping Cart**: Session-based cart management
- **Orders**: Complete order processing workflow
- **Reviews**: User review and rating system

**Key Models:**
- `Category` - Product categories
- `Company` - Brand management
- `Product` - Main product model with variants
- `ProductColor` - Color variants with individual stock
- `Cart` & `CartItem` - Shopping cart functionality
- `Order` & `OrderItem` - Order management

### User Auth App
Custom user authentication system:
- **Email-based Authentication**: No username required
- **Social Login**: Google OAuth2 integration
- **Profile Management**: Extended user profiles
- **Address Management**: Multiple shipping addresses

### Chatbot App
AI-powered customer assistance:
- **Ollama Integration**: Local AI model for recommendations
- **Session Management**: Persistent chat sessions
- **User Preferences**: Personalized shopping assistance
- **Product Recommendations**: Smart product suggestions

### Inventory ERP App
Comprehensive inventory management:
- **Device Catalog**: Complete device management with SKUs
- **Dealer Network**: Multi-tier dealer relationships
- **Purchase Management**: PO creation and tracking
- **Sales Processing**: Retail and wholesale sales
- **Payment Tracking**: Multi-method payment recording
- **Stock Control**: IMEI/Serial number tracking

## 🔧 Configuration

### Database Configuration
The application supports both SQLite (default) and PostgreSQL:

**SQLite (Development):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**PostgreSQL (Production):**
Set environment variables:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Social Authentication
To enable Google OAuth2:
1. Create Google OAuth2 credentials
2. Set environment variables:
   ```bash
   GOOGLE_OAUTH2_KEY=your-client-id
   GOOGLE_OAUTH2_SECRET=your-client-secret
   ```

### AI Chatbot Setup
The chatbot uses Ollama for AI responses:
1. Install Ollama locally
2. Pull required models (e.g., `ollama pull llama3`)
3. Ensure Ollama service is running

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

Access the modern admin interface at `/admin/` with superuser credentials.

**Features:**
- **Django Unfold**: Modern, responsive admin interface
- **Product Management**: Complete product catalog management
- **Order Processing**: Order management and tracking
- **User Management**: User accounts and permissions
- **Inventory Control**: Stock management and tracking
- **Analytics**: Basic reporting and analytics

## 🔗 API Endpoints

### Store API
- `GET /store/` - Product listing with filters
- `GET /store/product/<slug>/` - Product details
- `POST /store/add-to-cart/<id>/` - Add to cart
- `GET /store/api/product/<id>/colors/` - Product colors
- `GET /store/api/product/<id>/color/<id>/images/` - Color images

### Chatbot API
- `GET /chatbot/widget/` - Chat widget
- `POST /chatbot/message/` - Send chat message

### User API
- `POST /login/` - User login
- `POST /signup/` - User registration
- `GET /profile/` - User profile
- `GET /orders/` - User orders

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

## 🆘 Support

For support and questions:
- **Issues**: [GitHub Issues](https://github.com/Abdulwasay551/future-store/issues)
- **Documentation**: Check the `docs/` directory
- **Deployment**: See `DEPLOYMENT_GUIDE.md`

## 🚦 Status

- ✅ **Core E-commerce**: Fully functional
- ✅ **User Authentication**: Complete with social auth
- ✅ **Admin Interface**: Modern Django Unfold
- ✅ **Inventory ERP**: Comprehensive business management
- ✅ **AI Chatbot**: Ollama integration
- ✅ **Deployment**: Vercel-ready
- 🔄 **Testing**: Ongoing improvements
- 🔄 **Documentation**: Continuous updates

---

**Built with ❤️ using Django 5.2+ and modern web technologies**