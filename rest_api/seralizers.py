from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post, Category


class Post_serializer(serializers.ModelSerializer):
    photo = serializers.CharField()

    class Meta:
        model = Post
        fields = "__all__"


class Post_list_serializer(serializers.ModelSerializer):
    photo = serializers.CharField()
    like = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class Category_serializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class User_serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
