# Django Pizza Shop - Architecture Overview

## 🏗️ System Architecture

This application follows Django's **MVT (Model-View-Template)** architecture pattern with a clear separation of concerns.

## 📦 Application Structure

### 1. **Core App** (`core/`)
- **Purpose**: Main application entry point and common functionality
- **Responsibilities**:
  - Homepage view
  - Base URL routing
- **Models**: None
- **Views**: `home_view` - displays featured products and categories

### 2. **Accounts App** (`accounts/`)
- **Purpose**: User authentication and profile management
- **Responsibilities**:
  - User registration
  - User login/logout
  - User profile management
  - Role-based access control (Admin/Customer)
- **Models**:
  - `UserProfile`: Extends Django User with role, phone, address
- **Views**:
  - `register_view`: User registration
  - `login_view`: User authentication
  - `profile_view`: User profile display
- **Features**:
  - Automatic profile creation via Django signals
  - Role-based permissions
  - Integration with Django admin

### 3. **Products App** (`products/`)
- **Purpose**: Product and category management
- **Responsibilities**:
  - Product CRUD operations (Admin only)
  - Product listing (Public)
  - Category management
  - Product detail views
- **Models**:
  - `Category`: Pizza categories with slug for SEO-friendly URLs
  - `Product`: Pizza products with images, prices, availability
- **Views**:
  - `ProductListView`: List all available products with pagination
  - `ProductDetailView`: Individual product details
  - `ProductCreateView`: Admin-only product creation
  - `ProductUpdateView`: Admin-only product updates
  - `ProductDeleteView`: Admin-only product deletion
  - `category_detail`: Category-specific product listing
- **Features**:
  - Image upload support
  - Category filtering
  - Availability status
  - Admin-only CRUD operations

### 4. **Orders App** (`orders/`)
- **Purpose**: Shopping cart and order management
- **Responsibilities**:
  - Session-based cart management
  - Order placement
  - Order history
  - Order status management (Admin)
- **Models**:
  - `Order`: Customer orders with status tracking
  - `OrderItem`: Individual items in an order
- **Views**:
  - `cart_view`: Display shopping cart
  - `add_to_cart`: Add product to cart
  - `remove_from_cart`: Remove product from cart
  - `update_cart`: Update product quantity
  - `checkout`: Process order creation
  - `order_list`: Customer order history
  - `order_detail`: Order details view
  - `admin_order_list`: Admin view of all orders
  - `update_order_status`: Admin order status update
- **Context Processor**:
  - `cart`: Provides cart count and total to all templates
- **Features**:
  - Session-based cart (no database until checkout)
  - Order status workflow (Pending → Paid → Delivered/Cancelled)
  - Admin order management
  - Customer order tracking

## 🔄 Request Flow

### Customer Flow:
1. **Browse Products**: `core:home` → `products:product_list` → `products:product_detail`
2. **Add to Cart**: `orders:add_to_cart` (stores in session)
3. **View Cart**: `orders:cart`
4. **Checkout**: `orders:checkout` (creates Order in database)
5. **View Orders**: `orders:order_list` → `orders:order_detail`

### Admin Flow:
1. **Product Management**: `products:product_create/update/delete`
2. **Order Management**: `orders:admin_order_list` → `orders:update_order_status`
3. **Django Admin**: `/admin/` for full CRUD operations

## 🗄️ Database Schema

```
User (Django built-in)
  └── UserProfile (OneToOne)
      ├── role (customer/admin)
      ├── phone_number
      └── address

Category
  ├── name
  ├── slug
  └── description

Product
  ├── name
  ├── description
  ├── price
  ├── image
  ├── category (ForeignKey → Category)
  └── is_available

Order
  ├── customer (ForeignKey → User)
  ├── status (pending/paid/delivered/cancelled)
  ├── total_price
  └── timestamps

OrderItem
  ├── order (ForeignKey → Order)
  ├── product (ForeignKey → Product)
  ├── quantity
  └── price
```

## 🔐 Security Features

1. **CSRF Protection**: Enabled on all forms
2. **Authentication**: Django's built-in authentication system
3. **Authorization**: Role-based access control
   - `@login_required`: Requires authentication
   - `@user_passes_test(is_admin)`: Requires admin role
4. **Input Validation**: Django form validation + model validation
5. **SQL Injection Protection**: Django ORM (parameterized queries)
6. **XSS Protection**: Django template auto-escaping
7. **Session Security**: Secure session cookies in production

## 🎨 Frontend Architecture

### Template Hierarchy:
```
base.html (Base template with navbar/footer)
  ├── core/home.html
  ├── accounts/login.html
  ├── accounts/register.html
  ├── accounts/profile.html
  ├── products/product_list.html
  ├── products/product_detail.html
  ├── products/product_form.html
  ├── products/product_confirm_delete.html
  ├── products/category_detail.html
  ├── orders/cart.html
  ├── orders/order_list.html
  ├── orders/order_detail.html
  └── orders/admin_order_list.html
```

### Styling:
- **Bootstrap 5.3**: Responsive UI framework
- **Bootstrap Icons**: Icon library
- **Responsive Design**: Mobile-first approach

## 🔌 URL Routing

### Main URLs (`pizzashop/urls.py`):
- `/` → Core app
- `/accounts/` → Accounts app
- `/products/` → Products app
- `/orders/` → Orders app
- `/admin/` → Django admin

### URL Patterns:
- REST-like patterns (e.g., `/products/<id>/`, `/orders/<id>/`)
- Namespaced URLs for app isolation
- Query parameters for filtering (e.g., `?category=slug`)

## 📊 Data Flow

### Cart Management:
1. **Add to Cart**: Product → Session (no DB)
2. **Cart View**: Session → Display
3. **Checkout**: Session → Database (Order + OrderItems)
4. **Clear Cart**: Session cleared after successful checkout

### Order Processing:
1. **Checkout**: Creates Order with status='pending'
2. **Admin Updates**: Changes status (pending → paid → delivered)
3. **Customer Views**: Can see status updates in real-time

## 🚀 Scalability Considerations

### Current Design:
- Session-based cart (scales with user sessions)
- Database-backed orders (persistent storage)
- Image storage in filesystem (can migrate to S3/CDN)

### Future Enhancements:
- Redis for session storage (distributed systems)
- Celery for async tasks (email notifications)
- Caching layer (Redis/Memcached)
- CDN for static/media files
- Database connection pooling
- REST API with Django REST Framework

## 🧪 Testing Strategy

### Recommended Tests:
1. **Model Tests**: Test model methods and relationships
2. **View Tests**: Test authentication, authorization, redirects
3. **Form Tests**: Test validation and data processing
4. **Integration Tests**: Test complete user flows

### Test Coverage Areas:
- User registration and authentication
- Product CRUD operations
- Cart functionality
- Order creation and status updates
- Role-based access control

## 📝 Code Organization Principles

1. **DRY (Don't Repeat Yourself)**: Reusable templates, utility functions
2. **Separation of Concerns**: Each app has a single responsibility
3. **Modularity**: Apps are independent and can be extended
4. **Convention over Configuration**: Follows Django conventions
5. **Security First**: Built-in security features enabled by default

## 🔄 Workflow States

### Order Status Flow:
```
Pending → Paid → Delivered
         ↓
      Cancelled
```

### User Role Flow:
```
Registration → Customer (default)
            ↓
         Admin (via Django admin)
```

## 🎯 Key Design Decisions

1. **Session-based Cart**: Faster, no DB overhead until checkout
2. **UserProfile Extension**: Maintains Django User model, adds role via OneToOne
3. **Class-based Views**: Used for CRUD operations (DRY principle)
4. **Function-based Views**: Used for cart operations (simpler logic)
5. **Bootstrap UI**: Fast development, responsive, professional look
6. **PostgreSQL**: Production-ready, scalable, feature-rich

