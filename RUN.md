# 🚀 How to Run Django Pizza Shop

## Quick Setup (If PostgreSQL is configured)

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies (if not done)
pip install -r requirements.txt

# 3. Set up database (choose one method below)
# Method A: Use the setup script
./setup_database.sh

# Method B: Manual setup
sudo -u postgres psql
# Then in psql:
CREATE DATABASE pizzashop_db;
CREATE USER pizzashop_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE pizzashop_db TO pizzashop_user;
\q

# 4. Update .env file with correct database credentials

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Run server
python manage.py runserver
```

## Current Status

✅ **Completed:**
- Virtual environment created
- Dependencies installed
- .env file created with secret key
- Code fixed (admin views decorator issue)

❌ **Needs Action:**
- PostgreSQL database setup (password authentication issue)
- Database migrations
- Create superuser
- Set admin role

## Database Connection Issue

The application is trying to connect to PostgreSQL but the password authentication is failing.

### Option 1: Fix PostgreSQL Password

1. Find your PostgreSQL password or reset it:
```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'new_password';
\q
```

2. Update `.env` file with the correct password:
```env
DATABASE_PASSWORD=new_password
```

### Option 2: Use SQLite for Development (Quick Start)

If you want to test quickly without PostgreSQL, I can modify the settings to use SQLite temporarily. Just let me know!

### Option 3: Create New Database User

```bash
sudo -u postgres psql
CREATE DATABASE pizzashop_db;
CREATE USER pizzashop_user WITH PASSWORD 'pizzashop_pass';
GRANT ALL PRIVILEGES ON DATABASE pizzashop_db TO pizzashop_user;
\q
```

Then update `.env`:
```env
DATABASE_USER=pizzashop_user
DATABASE_PASSWORD=pizzashop_pass
```

## Next Steps After Database is Ready

1. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Start server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the app:**
   - Homepage: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

5. **Set admin role:**
   - Go to Django admin
   - Navigate to Accounts > User Profiles
   - Change your user's role to "Admin"

## Need Help?

If you're having trouble with PostgreSQL, I can:
1. Help you configure PostgreSQL properly
2. Switch to SQLite for quick testing
3. Create a setup script that handles everything

Let me know what you'd prefer!

