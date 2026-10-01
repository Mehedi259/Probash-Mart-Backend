from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<uuid:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('methods/', views.PaymentMethodListView.as_view(), name='payment-method-list'),
    path('methods/<uuid:pk>/', views.PaymentMethodDetailView.as_view(), name='payment-method-detail'),
]
