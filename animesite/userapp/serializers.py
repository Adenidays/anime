from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from animeapp.models import AnimeRating, Comment, AnimeList
from animeapp.serializers import AnimeRatingSerializer, CommentSerializer, AnimeListSerializer
from userapp.models import WishList, AnimeCollection, UserSubscription


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


class WishListSerializer(serializers.ModelSerializer):
    anime = AnimeListSerializer()

    class Meta:
        model = WishList
        fields = ['id', 'user', 'anime']


class WishListCreateSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=AnimeList.objects.all())

    class Meta:
        model = WishList
        fields = ['anime']

    def validate(self, data):
        anime = data.get('anime')

        if not AnimeList.objects.filter(pk=anime.pk).exists():
            raise serializers.ValidationError("Аниме с указанным идентификатором не существует.")

        return data


class AnimeCollectionSerializer(serializers.ModelSerializer):
    anime = AnimeListSerializer(many=True)

    class Meta:
        model = AnimeCollection
        fields = ['id', 'name', 'subscribers', 'anime', 'creator']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['collection']

    def create(self, validated_data):
        user = self.context['request'].user
        subscription = UserSubscription.objects.create(user=user, **validated_data)
        return subscription