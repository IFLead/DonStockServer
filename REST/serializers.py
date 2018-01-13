from rest_framework import serializers

from .models import Photo
from .models import Shop


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)


class ShopSerializer(serializers.ModelSerializer):
    photos = ImageSerializer(many=True, source='images')

    class Meta:
        model = Shop
        fields = '__all__'
