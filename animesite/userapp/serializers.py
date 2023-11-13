from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from animeapp.models import AnimeRating, Comment
from animeapp.serializers import AnimeRatingSerializer, CommentSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password', 'image')

    def validate(self, attrs):
        if 'image' not in attrs:
            attrs['image'] = None
        return super().validate(attrs)



class CustomUserSerializer(serializers.ModelSerializer):
    anime_ratings = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'image', 'anime_ratings', 'comments')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not self.context['request'].user.is_superuser:
            ret.pop('image', None)
        return ret

    def get_anime_ratings(self, user):
        ratings = AnimeRating.objects.filter(user=user)
        serializer = AnimeRatingSerializer(ratings, many=True)
        return serializer.data

    def get_comments(self, user):
        user_comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(user_comments, many=True)
        return serializer.data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(required=True)


class ChangeEmailSerializer(serializers.Serializer):
    old_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    new_email = serializers.CharField(required=True)
