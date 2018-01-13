from django.contrib import admin
from .models import Shop
from .models import Photo
from .models import Category

# Register your models here.
admin.site.register(Shop)
admin.site.register(Photo)
admin.site.register(Category)
