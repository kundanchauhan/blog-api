from rest_framework import serializers

from .models import BlogUser, CreatePost


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active')


class CreatePostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CreatePost
        fields = ('user', 'username', 'title', 'description', 'state','is_active')



