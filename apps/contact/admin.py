from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_resolved', 'created_at']
    list_filter = ['is_read', 'is_resolved']
    search_fields = ['name', 'email', 'subject']
