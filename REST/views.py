import base64

from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Voting.models import Vote
from .models import Category, Photo
from .models import Shop
from .serializers import CategorySerializer
from .serializers import ShopSerializer


# Create your views here.
class ShopList(APIView):
	def get(self, request):
		shops = Shop.objects.all().order_by('-rating', '-likes', 'dislikes')[:8]
		serializer = ShopSerializer(shops, many=True, context={"request": request})
		content_type = ContentType.objects.get_for_model(Shop)
		shops = serializer.data
		token = Token.objects.filter(key=request._request.GET.get('token'))
		if len(token) > 0:
			votes = Vote.objects.filter(user_id=token[0].user, content_type=content_type).values('object_id',
				'action')
			user_votes = {vote['object_id']: vote['action'] for vote in votes}
			# todo: fix bag with vote status
			for shop in shops:
				shop['vote_status'] = user_votes.get(shop['id'], 0)
		return Response(shops)


class Categories(APIView):
	def get(self, request):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		categories = serializer.data
		return Response(categories)


class Votes(APIView):
	def post(self, request):
		# if if_authorized(request.user) and 'action' in request.POST and 'shop' in request.POST:
		token = Token.objects.filter(key=request.data.get('token'))
		if len(token) > 0:
			user_id = token[0].user.id
			action = request.data.get('action')
			shop_id = request.data.get('shop')
			try:
				shop = Shop.objects.get(id=shop_id)
			except:
				return Response({'status': 'Invalid data'})
			if action:
				status = shop.votes.up(user_id)
			else:
				status = shop.votes.down(user_id)

			return Response(
				{'status': 'OK', 'rating': shop.rating, 'likes': shop.likes,
					'dislikes': shop.dislikes, 'vote_status': status[1]})
		else:
			return Response({'status': 'Invalid data'})


class LogoutSessionView(APIView):

	def post(self, request, *args, **kwargs):
		logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)


def if_authorized(user):
	if user.is_authenticated:
		return user.get_full_name()
	return False


@csrf_exempt
@api_view(['POST'])
def append_shops(request):
	ids = request.data.get('ids')
	shops = Shop.objects.exclude(id__in=ids).order_by('-rating', '-likes', 'dislikes')[:8]
	serializer = ShopSerializer(shops, many=True, context={"request": request})
	shops = serializer.data
	return Response(shops)


@csrf_exempt
@api_view(['POST'])
def add_shop(request):
	token = Token.objects.filter(key=request.data.get('token'))
	if len(token) > 0:
		shop = Shop()
		shop.name = request.data.get('name')
		shop.link_one = request.data.get('link_one')
		shop.link_two = request.data.get('link_two')
		shop.link_three = request.data.get('link_three')
		shop.user = token[0].user
		shop.description = request.data.get('description')
		# array_serializer = ArraySerializer(data=request.data.get('categories'))
		# array_serializer.is_valid(raise_exception=True)
		# categories = array_serializer.data.get('categories_array')
		shop.save()

		for data in request.data.get('mainPhoto')[:1] + request.data.get('otherPhotos')[:9]:
			format, imgstr = data['dataURL'].split(';base64,')
			new = Photo()
			# todo: may be replace old photo
			new.photo = ContentFile(base64.b64decode(imgstr), name=data['upload']['filename'])
			new.shop = shop
			new.save()

		shop.categories.add(*request.data.get('categories'))
		shop.save()

		shops = Shop.objects.filter(id__exact=shop.id)
		serializer = ShopSerializer(shops, many=True, context={"request": request})
		shops = serializer.data
		return Response({"status": True, **shops[0]})
	else:
		return Response({"status": False})


@csrf_exempt
@api_view(['POST'])
def check_token(request):
	token = Token.objects.filter(key=request.data.get('token'))
	return Response({"status": len(token) > 0})


@csrf_exempt
@api_view(['GET'])
def get_all_shops_for_user(request):
	token = Token.objects.filter(key=request._request.GET.get('token'))
	if len(token) > 0:
		shops = Shop.objects.filter(user_id=token[0].user_id).order_by('-rating', '-likes', 'dislikes')[:8]
		serializer = ShopSerializer(shops, many=True, context={"request": request})
		content_type = ContentType.objects.get_for_model(Shop)
		shops = serializer.data
		votes = Vote.objects.filter(user_id=token[0].user, content_type=content_type).values('object_id',
																							 'action')
		user_votes = {vote['object_id']: vote['action'] for vote in votes}
		# todo: fix bag with vote status
		for shop in shops:
			shop['vote_status'] = user_votes.get(shop['id'], 0)
		return Response(shops)
