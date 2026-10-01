from django.contrib import admin
from .models import Transaction, PaymentMethod

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method']
    search_fields = ['transaction_id']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'sort_order']
