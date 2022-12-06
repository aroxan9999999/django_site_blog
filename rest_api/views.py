from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from blog.models import Post, Category
from rest_api.seralizers import Post_serializer, Category_serializer, User_serializer, Post_list_serializer
from rest_framework.permissions import *


class Postapi(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = Post_serializer
    permission_classes = (IsAdminUser,)


class Catefory_api(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_serializer
    permission_classes = (IsAdminUser,)


class User_api(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User_serializer
    permission_classes = (IsAdminUser,)


class Post_list(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = Post_list_serializer
    permission_classes = (IsAuthenticated,)


class Catefory_list(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = Category_serializer
    permission_classes = (IsAuthenticated,)

