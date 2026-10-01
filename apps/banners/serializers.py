from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'image', 'link', 'position',
                  'is_active', 'sort_order', 'clicks', 'starts_at', 'ends_at', 'created_at']
