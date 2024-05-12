from rest_framework import serializers
from django.utils import timezone

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_date_of_manufacture(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Manufacture date cannot be in the future")
        return value
