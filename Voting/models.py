from math import sqrt

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType

UP = 1
NO = 0
DOWN = -1


class VoteManager(models.Manager):
	def filter(self, *args, **kwargs):
		if 'content_object' in kwargs:
			content_object = kwargs.pop('content_object')
			content_type = ContentType.objects.get_for_model(content_object)
			kwargs.update({
				'content_type': content_type,
				'object_id': content_object.pk
			})

		return super(VoteManager, self).filter(*args, **kwargs)


VOTES_CHOICES = (
	(UP, 'Like'),
	(NO, '-'),
	(DOWN, 'Dislike'),
)


class Vote(models.Model):
	ACTION_FIELD = {
		UP: 'likes',
		DOWN: 'dislikes'
	}

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()
	action = models.SmallIntegerField(default=NO, choices=VOTES_CHOICES)
	created = models.DateTimeField(auto_now=True)

	objects = VoteManager()

	class Meta:
		unique_together = ('user', 'content_type', 'object_id', 'action')
		index_together = ('content_type', 'object_id')
		verbose_name = 'Голос'
		verbose_name_plural = 'Голоса'

	@classmethod
	def votes_for(cls, model, instance=None, action=NO):
		ct = ContentType.objects.get_for_model(model)
		kwargs = {
			"content_type": ct,
			"action": action
		}
		if instance is not None:
			kwargs["object_id"] = instance.pk

		return cls.objects.filter(**kwargs)


from .managers import VotableManager


class VoteModel(models.Model):
	likes = models.PositiveIntegerField('Лайки', default=0, db_index=True)
	dislikes = models.PositiveIntegerField('Дизайки', default=0, db_index=True)
	votes = VotableManager()

	class Meta:
		abstract = True

	# def save(self, *args, **kwargs):
	#     super(VoteModel, self).save(*args, **kwargs)

	@property
	def count(self):
		return self.likes + self.dislikes

	@property
	def calculate_vote_score(self):
		ups = self.likes
		downs = self.dislikes
		n = ups + downs

		if n == 0:
			return 0

		z = 1.281551565545
		p = float(ups) / n

		left = p + 1 / (2 * n) * z * z
		right = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
		under = 1 + 1 / n * z * z

		return int(round((left - right) / under * 100, 0))

		# return int(round(self.likes / (self.likes + self.dislikes) * 100, 0))

		# @property
		# def is_voted_up(self):
		#     try:
		#         return self._is_voted_up
		#     except AttributeError:
		#         return False
		#
		# @is_voted_up.setter
		# def is_voted_up(self, value):
		#     self._is_voted_up = value
		#
		# @property
		# def is_voted_down(self):
		#     try:
		#         return self._is_voted_down
		#     except AttributeError:
		#         return False
		#
		# @is_voted_down.setter
		# def is_voted_down(self, value):
		#     self._is_voted_down = value
