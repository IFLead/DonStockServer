from rest_framework import serializers

from .models import Photo
from .models import Shop


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('url',)

    def get_url(self, car):
        request = self.context.get('request')
        photo_url = car.photo.url
        return request.build_absolute_uri(photo_url)


class ShopSerializer(serializers.ModelSerializer):
    photos = ImageSerializer(many=True, source='images')

    class Meta:
        model = Shop
        fields = '__all__'
