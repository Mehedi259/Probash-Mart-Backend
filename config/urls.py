from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Root → API Docs
    path('', RedirectView.as_view(url='/api/docs/', permanent=False), name='root'),

    # Django Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 Endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/categories/', include('apps.products.urls_categories')),
    path('api/v1/cart/', include('apps.cart.urls')),
    path('api/v1/wishlist/', include('apps.wishlist.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/coupons/', include('apps.coupons.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/banners/', include('apps.banners.urls')),
    path('api/v1/blog/', include('apps.blog.urls')),
    path('api/v1/pages/', include('apps.pages.urls')),
    path('api/v1/shipping/', include('apps.shipping.urls')),
    path('api/v1/contact/', include('apps.contact.urls')),
    path('api/v1/newsletter/', include('apps.newsletter.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
