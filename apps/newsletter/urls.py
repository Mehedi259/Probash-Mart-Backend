from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='newsletter-subscribe'),
    path('unsubscribe/<str:email>/', views.UnsubscribeView.as_view(), name='newsletter-unsubscribe'),
    path('admin/list/', views.AdminSubscriberListView.as_view(), name='admin-subscriber-list'),
]
