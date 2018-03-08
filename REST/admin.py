from django.contrib import admin

from Voting.models import Vote
from .models import Shop
from .models import Photo
from .models import Category

# Register your models here.
admin.site.register(Shop)
admin.site.register(Photo)
admin.site.register(Category)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'content_object', 'created')
