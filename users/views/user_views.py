
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserDeleteSerializer


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
