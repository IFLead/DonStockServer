from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Voting.models import Vote
from .models import Shop
from .models import Category
from .serializers import ShopSerializer
from .serializers import CategorySerializer


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

    @method_decorator(login_required)
    def post(self, request, format=None):
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


def if_authorized(user):
    if user.is_authenticated:
        return user.get_full_name()
    return False


@csrf_exempt
@api_view(['POST'])
def check_token(request, format=None):
    token = Token.objects.filter(key=request.data['token'])
    return JsonResponse({"status": len(token) > 0})
