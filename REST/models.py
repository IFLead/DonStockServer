from django.contrib.auth.models import User
from django.db import models

from Voting.models import VoteModel


# Create your models here.

class Category(models.Model):
	name = models.CharField('Название', blank=False, null=True, max_length=64)

	def __str__(self):
		self.name = self.name
		return self.name

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Shop(VoteModel, models.Model):
	name = models.CharField('Название', blank=False, null=True, max_length=64)
	link_one = models.URLField('Первая ссылка', blank=False, null=True, max_length=255)
	link_two = models.URLField('Вторая ссылка', blank=True, max_length=255)
	link_three = models.URLField('Третья ссылка', blank=True, max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField('Описание', blank=False, null=True, max_length=245)
	categories = models.ManyToManyField(Category, related_name='shops', verbose_name='Категории')
	rating = models.DecimalField('Общий рейтинг', default=0, decimal_places=2, max_digits=10)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Магазин'
		verbose_name_plural = 'Магазины'


class Photo(models.Model):
	photo = models.ImageField('Изображание магазина', upload_to='shops-images/%Y/%m/%d')

	shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='images', blank=True, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Фотография'
		verbose_name_plural = 'Фотографии'
