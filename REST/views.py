from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from Voting.models import Vote, UP, DOWN
from .models import Shop
from .serializers import ShopSerializer


# Create your views here.
class ShopList(APIView):
	def get(self, request):
		shops = Shop.objects.all()
		serializer = ShopSerializer(shops, many=True, context={"request": request})
		content_type = ContentType.objects.get_for_model(Shop)
		shops = serializer.data
		if not request.user.is_authenticated:
			votes = Vote.objects.filter(user_id=request.user.id, content_type=content_type).values('object_id', 'action')
			user_votes = {vote['object_id']: vote['action'] for vote in votes}
			for shop in shops:
				shop['vote_status'] = 0 if shop['id'] not in user_votes else user_votes[shop['id']]
			return Response(shops)


@permission_classes((IsAuthenticated, ))
class Votes(APIView):
	def post(self, request, format=None):
		if 'action' in request.POST and 'shop' in request.POST:
			action = json.loads(request.POST.get('action'))
			shop_id = request.POST.get('shop', -1)
			try:
				shop = Shop.objects.get(id=shop_id)
			except:
				return JsonResponse({'status': 'Invalid data'})
			if action:
				status = shop.votes.up(request.user.id)
			else:
				status = shop.votes.down(request.user.id)
			return JsonResponse(
				{'status': 'OK', 'rating': shop.calculate_vote_score, 'likes': shop.likes,
					'dislikes': shop.dislikes, 'vote_status': status[1]})

