# Probash Mart Backend API

Industry-grade REST API built with **Django REST Framework** powering both the Probash Mart customer website and the admin dashboard.

## 🚀 Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Access API docs
open http://localhost:8000/api/docs/
```

## 🔑 Default Credentials

- **Admin**: `admin@probashmart.com` / `admin123`
- **API Docs**: http://localhost:8000/api/docs/ (Swagger UI)
- **ReDoc**: http://localhost:8000/api/redoc/
- **Django Admin**: http://localhost:8000/admin/

## 📊 API Overview (69 Endpoints)

### 🔐 Authentication (`/api/v1/auth/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register/` | Register new customer |
| POST | `/login/` | JWT Login (returns access + refresh tokens) |
| POST | `/token/refresh/` | Refresh JWT token |
| POST | `/logout/` | Blacklist refresh token |
| GET/PUT | `/profile/` | Get/update user profile |
| POST | `/change-password/` | Change password |
| GET | `/customers/` | Admin: List all customers |
| GET/POST | `/users/` | Admin: Manage admin users |
| GET/PUT/DELETE | `/users/{id}/` | Admin: User detail |

### 🛍️ Products (`/api/v1/products/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List products (search, filter, paginate) |
| GET | `/featured/` | Homepage featured products |
| GET | `/best-sellers/` | Best selling products |
| GET | `/flash-deals/` | Flash deal products |
| GET | `/category/{slug}/` | Products by category |
| GET | `/{slug}/` | Product detail |
| GET/POST | `/admin/list/` | Admin: Product CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Product detail |
| POST | `/admin/{id}/images/` | Admin: Upload gallery images |

### 📂 Categories (`/api/v1/categories/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List active categories |
| GET/POST | `/admin/list/` | Admin: Category CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Category detail |

### 🛒 Cart (`/api/v1/cart/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/` | List cart / Add to cart |
| PUT | `/{id}/update/` | Update quantity |
| DELETE | `/{id}/delete/` | Remove item |
| DELETE | `/clear/` | Clear entire cart |

### ❤️ Wishlist (`/api/v1/wishlist/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/` | List / Add to wishlist |
| POST | `/toggle/` | Toggle wishlist item |
| DELETE | `/{id}/delete/` | Remove from wishlist |

### 📦 Orders (`/api/v1/orders/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create/` | Place order (checkout) |
| GET | `/my-orders/` | Customer order history |
| GET | `/my-orders/{id}/` | Order detail |
| GET | `/track/{order_number}/` | Track order (public) |
| GET | `/admin/list/` | Admin: All orders |
| GET/PUT | `/admin/{id}/` | Admin: Update status |

### 💳 Payments (`/api/v1/payments/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions/` | Admin: List transactions |
| GET | `/transactions/{id}/` | Admin: Transaction detail |
| GET/POST | `/methods/` | Payment methods |
| GET/PUT/DELETE | `/methods/{id}/` | Payment method detail |

### 🏷️ Coupons (`/api/v1/coupons/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/validate/` | Validate coupon at checkout |
| GET/POST | `/admin/list/` | Admin: Coupon CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Coupon detail |

### ⭐ Reviews (`/api/v1/reviews/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/product/{id}/` | Product reviews |
| GET | `/admin/list/` | Admin: All reviews |
| PUT | `/admin/{id}/moderate/` | Admin: Approve/reject |
| DELETE | `/admin/{id}/delete/` | Admin: Delete review |

### 🖼️ Banners (`/api/v1/banners/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Active banners (filter by position) |
| GET/POST | `/admin/list/` | Admin: Banner CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Banner detail |

### 📝 Blog (`/api/v1/blog/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Published posts |
| GET | `/{slug}/` | Post detail |
| GET/POST | `/admin/list/` | Admin: Blog CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Post detail |

### 📄 Pages (`/api/v1/pages/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/{slug}/` | Static page content |
| GET/POST | `/admin/list/` | Admin: Page CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Page detail |

### 🚚 Shipping (`/api/v1/shipping/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Active shipping zones |
| GET/POST | `/admin/list/` | Admin: Zone CRUD |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Zone detail |

### 📧 Contact (`/api/v1/contact/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/submit/` | Submit contact form |
| GET | `/admin/list/` | Admin: Messages list |
| GET/PUT/DELETE | `/admin/{id}/` | Admin: Message detail |

### 📬 Newsletter (`/api/v1/newsletter/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/subscribe/` | Subscribe |
| DELETE | `/unsubscribe/{email}/` | Unsubscribe |
| GET | `/admin/list/` | Admin: Subscribers |

### 📊 Analytics (`/api/v1/analytics/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/` | Dashboard metrics |
| GET | `/sales/` | Sales chart data |
| GET | `/orders-by-status/` | Order status breakdown |
| GET | `/top-products/` | Top selling products |
| GET | `/overview/` | Conversion rate, AOV |

## 🏗️ Project Structure

```
Probash-Mart-Backend/
├── config/                  # Django project settings
│   ├── settings.py          # Main settings (JWT, CORS, DRF, etc.)
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI entry point
├── apps/                    # All Django apps
│   ├── core/                # Base models, permissions, pagination
│   ├── accounts/            # Custom User, auth, admin users
│   ├── products/            # Products, Categories, Gallery
│   ├── orders/              # Orders, OrderItems
│   ├── cart/                # Server-side shopping cart
│   ├── wishlist/            # User wishlist
│   ├── payments/            # Transactions, Payment methods
│   ├── coupons/             # Discount codes
│   ├── reviews/             # Product reviews with moderation
│   ├── banners/             # Promotional banners
│   ├── blog/                # Blog posts
│   ├── pages/               # Static content pages
│   ├── analytics/           # Dashboard metrics & reports
│   ├── shipping/            # Shipping zones & fees
│   ├── contact/             # Contact form
│   └── newsletter/          # Email subscriptions
├── media/                   # Uploaded files
├── staticfiles/             # Collected static files
├── venv/                    # Python virtual environment
├── .env                     # Environment variables
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## ⚙️ Tech Stack

- **Python 3.14** + **Django 6.1**
- **Django REST Framework 3.18** (API)
- **SimpleJWT** (Authentication)
- **drf-spectacular** (OpenAPI/Swagger docs)
- **django-filter** (Advanced filtering)
- **django-cors-headers** (CORS)
- **WhiteNoise** (Static files)
- **Gunicorn** (Production server)
- **SQLite** (dev) / **PostgreSQL** (production-ready)
- **Docker** (Containerization)

## 🔒 Security Features

- JWT token authentication with refresh/blacklist
- Role-based access control (Customer, Manager, Editor, Super Admin)
- Rate limiting (100/hr anon, 1000/hr authenticated)
- CORS whitelisting
- Production HSTS, SSL redirect, secure cookies
- Password validation
- UUID primary keys (non-guessable)
