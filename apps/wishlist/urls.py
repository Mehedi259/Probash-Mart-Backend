from django.urls import path
from . import views

urlpatterns = [
    path('', views.WishlistListView.as_view(), name='wishlist-list'),
    path('<uuid:pk>/delete/', views.WishlistDeleteView.as_view(), name='wishlist-delete'),
    path('toggle/', views.WishlistToggleView.as_view(), name='wishlist-toggle'),
]
