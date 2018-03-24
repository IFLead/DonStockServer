from rest_framework import serializers

from .models import Photo, Category as CategoryModel
from .models import Shop


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('url',)

    # def get_url(self, car):
    #     request = self.context.get('request')
    #     photo_url = car.photo.url
    #     return request.build_absolute_uri(photo_url)
    def get_url(self, shop):
        photo_url = shop.photo.url
        return photo_url


class ShopSerializer(serializers.ModelSerializer):
    photos = ImageSerializer(many=True, source='images')

    class Meta:
        model = Shop
        fields = '__all__'

    def create(self, validated_data):
        shop = Shop.objects.create(**validated_data)
        return shop


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = CategoryModel
        fields = '__all__'


class ArraySerializer(serializers.Serializer):
    # Gets a list of Integers
    categories_array = serializers.ListField(child=serializers.IntegerField())
