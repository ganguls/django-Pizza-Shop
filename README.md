# Django Pizza Shop

A complete Pizza Shop Management System built with Django, PostgreSQL, and Bootstrap. This application provides a full-featured e-commerce platform for managing a pizza shop with separate interfaces for administrators and customers.

## 🎯 Features

### For Customers
- User registration and authentication
- Browse pizza menu with categories
- View detailed product information
- Add products to shopping cart
- Place orders
- View order history
- Track order status

### For Administrators
- All customer features
- Add, update, and delete pizza products
- Manage product categories
- View all customer orders
- Update order status (Pending, Paid, Delivered, Cancelled)
- Access to Django admin panel

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.0+
- **Database**: PostgreSQL
- **Frontend**: Django Templates (HTML)
- **Styling**: Bootstrap 5.3
- **Authentication**: Django built-in authentication
- **ORM**: Django ORM
- **Admin Panel**: Django Admin

## 📁 Project Structure

```
django-Pizza-Shop/
├── pizzashop/              # Main project directory
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── accounts/               # User authentication app
│   ├── models.py          # UserProfile model
│   ├── views.py           # Authentication views
│   ├── urls.py            # Account URLs
│   └── admin.py           # Admin configuration
├── products/               # Product management app
│   ├── models.py          # Category and Product models
│   ├── views.py           # Product views (CRUD)
│   ├── urls.py            # Product URLs
│   └── admin.py           # Admin configuration
├── orders/                 # Order management app
│   ├── models.py          # Order and OrderItem models
│   ├── views.py           # Cart and order views
│   ├── urls.py            # Order URLs
│   ├── admin.py           # Admin configuration
│   └── context_processors.py  # Cart context processor
├── core/                   # Core app
│   ├── views.py           # Homepage view
│   └── urls.py            # Core URLs
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── core/              # Core templates
│   ├── accounts/          # Authentication templates
│   ├── products/          # Product templates
│   └── orders/            # Order templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd django-Pizza-Shop
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

1. Create a PostgreSQL database:

```bash
sudo -u postgres psql
CREATE DATABASE pizzashop_db;
CREATE USER pizzashop_user WITH PASSWORD 'your_password';
ALTER ROLE pizzashop_user SET client_encoding TO 'utf8';
ALTER ROLE pizzashop_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pizzashop_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pizzashop_db TO pizzashop_user;
\q
```

### Step 5: Configure Environment Variables

1. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

2. Edit `.env` file with your settings:

```env
SECRET_KEY=your-secret-key-here-generate-a-random-string
DEBUG=True
DATABASE_NAME=pizzashop_db
DATABASE_USER=pizzashop_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Important**: Generate a secure secret key:
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user. After creation, you can:
1. Log in to Django admin panel
2. Go to User Profiles and set your user's role to "Admin"

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 9: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 👤 User Roles Setup

### Creating an Admin User

1. Register a new user through the website or Django admin
2. Go to Django admin panel: `http://127.0.0.1:8000/admin/`
3. Navigate to **Accounts > User Profiles**
4. Find your user and change the role to "Admin"
5. Save the changes

### Creating a Customer User

1. Register through the website registration page
2. By default, new users are created as "Customer" role
3. Customers can browse products, add to cart, and place orders

## 📊 Database Models

### UserProfile
- Extends Django User model
- Role: Admin or Customer
- Phone number and address fields

### Category
- Name and description
- Slug for URLs
- Timestamps

### Product
- Name, description, price
- Image upload
- Category (ForeignKey)
- Availability status

### Order
- Customer (ForeignKey to User)
- Status: Pending, Paid, Delivered, Cancelled
- Total price
- Timestamps

### OrderItem
- Order (ForeignKey)
- Product (ForeignKey)
- Quantity and price per item

## 🔐 Security Features

- CSRF protection enabled
- Secure password handling (Django's built-in validators)
- Role-based access control
- Input validation
- Environment variables for secrets
- Session security settings
- SQL injection protection (Django ORM)

## 🎨 Admin Panel Features

Access the admin panel at `/admin/` with your superuser credentials.

**Available Models:**
- Users and User Profiles
- Categories
- Products
- Orders and Order Items

**Admin Capabilities:**
- Full CRUD operations on all models
- Order status management
- User role management
- Product availability control

## 📝 Sample Data

You can add sample data through the Django admin panel:

1. **Create Categories:**
   - Classic Pizzas
   - Specialty Pizzas
   - Vegetarian Pizzas
   - Desserts

2. **Create Products:**
   - Add pizza products with images, descriptions, and prices
   - Assign categories
   - Set availability status

## 🧪 Testing the Application

### As a Customer:
1. Register a new account
2. Browse products
3. Add items to cart
4. Place an order
5. View order history

### As an Admin:
1. Log in with admin account
2. Add/edit/delete products
3. View all orders
4. Update order statuses

## 🐛 Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `.env`
- Ensure database exists and user has proper permissions

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Verify static files directory exists

### Media Files Not Loading
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings.py
- Ensure `media/` directory exists and is writable
- Verify URL configuration includes media serving in development

### Migration Issues
- Delete migration files (except `__init__.py`) and run `makemigrations` again
- Check for model syntax errors
- Ensure database is accessible

## 📚 API Endpoints (Future Enhancement)

The application is structured to easily add REST API endpoints using Django REST Framework in the future.

## 🚀 Deployment Considerations

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production-grade WSGI server (Gunicorn)
4. Set up a reverse proxy (Nginx)
5. Configure SSL/HTTPS
6. Use a production database (consider connection pooling)
7. Set up proper logging
8. Configure static file serving
9. Use environment variables for all secrets
10. Set up database backups

## 📄 License

This project is created for educational and learning purposes.

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Accessing Django Shell
```bash
python manage.py shell
```

## 🤝 Contributing

This is a learning project. Feel free to fork and modify as needed.

## 📞 Support

For issues or questions, please check the Django documentation or create an issue in the repository.

---

**Built with ❤️ using Django**
