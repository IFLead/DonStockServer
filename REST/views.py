from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Voting.models import Vote
from .models import Category
from .models import Shop
from .serializers import CategorySerializer
from .serializers import ShopSerializer
from .serializers import ArraySerializer


# Create your views here.
class ShopList(APIView):
	def get(self, request):
		shops = Shop.objects.all()
		serializer = ShopSerializer(shops, many=True, context={"request": request})
		content_type = ContentType.objects.get_for_model(Shop)
		shops = serializer.data
		if request.user.is_authenticated:
			votes = Vote.objects.filter(user_id=request.user.id, content_type=content_type).values('object_id',
				'action')
			user_votes = {vote['object_id']: vote['action'] for vote in votes}
			for shop in shops:
				shop['vote_status'] = 0 if shop['id'] not in user_votes else user_votes[shop['id']]
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
		action = request.data.get('action')
		shop_id = request.data.get('shop')
		try:
			shop = Shop.objects.get(id=shop_id)
		except:
			return Response({'status': 'Invalid data'})
		if action:
			status = shop.votes.up(request.user.id)
		else:
			status = shop.votes.down(request.user.id)
		return Response(
			{'status': 'OK', 'rating': shop.calculate_vote_score, 'likes': shop.likes,
				'dislikes': shop.dislikes, 'vote_status': status[1]})


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
def add_shop(request):
	token = Token.objects.filter(key=request.data.get('token'))
    if len(token) > 0:
		name = request.data.get('name')
		link_one = request.data.get('link_one')
		link_two = request.data.get('link_two')
		link_three = request.data.get('link_three')
		user = token[0].user
		description = request.data.get('description')
		array_serializer = ArraySerializer(data = request.data.get('categories'))
		categories = array_serializer.data.get('categories_array')Shop.objects.create(name=name, link_one=link_one, link_two=link_two, link_three=link_three, user=user,
			description=description, categories=categories)
		return Response({"status": True})
	else:
		return Response({"status": False})


@csrf_exempt
@api_view(['POST'])
def check_token(request):
    token = Token.objects.filter(key=request.data.get('token'))
    return Response({"status": len(token) > 0})
