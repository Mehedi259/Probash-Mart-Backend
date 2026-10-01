from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartListView.as_view(), name='cart-list'),
    path('<uuid:pk>/update/', views.CartItemUpdateView.as_view(), name='cart-item-update'),
    path('<uuid:pk>/delete/', views.CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('clear/', views.CartClearView.as_view(), name='cart-clear'),
]
