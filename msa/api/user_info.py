from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework.decorators import authentication_classes, api_view
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import F, OrderBy
from .parent import *


class NullsLastOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        values = super().get_ordering(request, queryset, view)
        return (OrderBy(F(value.lstrip("-")), descending=value.startswith("-"), nulls_last=True) for value in values)


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # fields = '__all__'
        exclude = ['groups', 'user_permissions', 'email', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(email=None, **validated_data)
        return user


@authentication_classes([SessionCsrfExemptAuthentication])
class UserViewSet(CustomViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = userSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, NullsLastOrderingFilter]
    search_fields = ['username']
    ordering = ['-last_login', '-id']


    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(http_method_names=['POST'])
@authentication_classes([SessionCsrfExemptAuthentication])
def login_request(request):
    # data = json.loads(request.data)
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    # print(user)
    if user is not None:
        login(request, user)
        User = get_user_model()
        user = User.objects.get(username=username)
        user_data = userSerializer(user, many=False).data

        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            "id": user.id,
            "exp": int(round(dt.timestamp()))
        }, settings.SECRET_KEY, algorithm='HS256')
        user_data["token"] = token

        return Response(user_data, status=status.HTTP_200_OK)
    else:
        return Response({'details': 'Incorrect Login credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(http_method_names=['POST'])
@authentication_classes([SessionCsrfExemptAuthentication])
def logout_request(request):
    print(request.user)
    username = request.user.username
    if not request.user.is_authenticated:
        return Response({'details': 'Incorrect Logout credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    logout(request)
    return Response({'details': '%s logged out.' % username}, status=status.HTTP_200_OK)
