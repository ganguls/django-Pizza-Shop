# 🚀 Quick Start Guide - Django Pizza Shop

## Prerequisites Check

Before starting, ensure you have:
- Python 3.10+ installed
- PostgreSQL installed and running
- pip (Python package manager)

Check versions:
```bash
python3 --version
psql --version
```

## Step-by-Step Setup

### 1. Navigate to Project Directory
```bash
cd /home/vvii/DEVs/django-Pizza-Shop
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up PostgreSQL Database

#### Option A: Using psql (Recommended)
```bash
sudo -u postgres psql
```

Then in PostgreSQL prompt:
```sql
CREATE DATABASE pizzashop_db;
CREATE USER pizzashop_user WITH PASSWORD 'your_password_here';
ALTER ROLE pizzashop_user SET client_encoding TO 'utf8';
ALTER ROLE pizzashop_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pizzashop_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pizzashop_db TO pizzashop_user;
\q
```

#### Option B: Using createdb command
```bash
sudo -u postgres createdb pizzashop_db
sudo -u postgres createuser pizzashop_user
sudo -u postgres psql -c "ALTER USER pizzashop_user WITH PASSWORD 'your_password_here';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE pizzashop_db TO pizzashop_user;"
```

### 6. Configure Environment Variables

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` file with your editor:
```bash
nano .env
# or
vim .env
```

Update the values:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=pizzashop_db
DATABASE_USER=pizzashop_user
DATABASE_PASSWORD=your_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generate a secure SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copy the output and paste it as `SECRET_KEY` in `.env`

### 7. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Admin User (Superuser)
```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: (enter a username)
- Email: (optional, press Enter to skip)
- Password: (enter a secure password)
- Password (again): (confirm password)

### 9. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 10. Set Admin Role (Important!)

1. Start the server (see next step)
2. Go to: http://127.0.0.1:8000/admin/
3. Login with your superuser credentials
4. Navigate to **Accounts > User Profiles**
5. Find your user and click on it
6. Change **Role** from "Customer" to "Admin"
7. Click **Save**

### 11. Run Development Server
```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 12. Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Products**: http://127.0.0.1:8000/products/

## 🎯 Quick Test

1. **Register a customer account**: http://127.0.0.1:8000/accounts/register/
2. **Add some products** (as admin): http://127.0.0.1:8000/admin/
   - Go to Products > Add Product
   - Create a category first if needed
3. **Browse products**: http://127.0.0.1:8000/products/
4. **Add to cart and checkout** (as customer)

## 🔧 Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if not running
sudo systemctl start postgresql
```

### Migration Errors
```bash
# If migrations fail, try:
python manage.py makemigrations --empty accounts
python manage.py makemigrations --empty products
python manage.py makemigrations --empty orders
python manage.py migrate
```

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 8001
```

### Module Not Found Errors
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## 🎉 You're Ready!

The application is now running. Start by:
1. Adding categories in Django admin
2. Adding products
3. Registering as a customer
4. Testing the full order flow

Happy coding! 🍕

