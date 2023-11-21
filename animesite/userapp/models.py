from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

from animeapp.models import AnimeList

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, image=None, **extra_fields):
        if not email:
            raise ValueError('The email is required to create this user')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, image=image, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, image=None, **extra_fields):
        user = self.create_user(email, password, username=username, image=image, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField("Email", unique=True)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    username = models.CharField("User Name", max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}-{self.pk}"

    groups = models.ManyToManyField(Group, related_name="userapp_users")
    user_permissions = models.ManyToManyField(Permission, related_name="userapp_users")

    class Meta:
        permissions = [
            ("can_change_user_permissions", "Can change user permissions"),
        ]
        default_permissions = ()


class AnimeCollection(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='collection_image/', blank=True, null=True)
    subscribers = models.PositiveIntegerField(default=0)
    anime = models.ManyToManyField(AnimeList)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.pk}'


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(AnimeCollection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} подписан на {self.collection.name}"

    class Meta:
        unique_together = ('user', 'collection')


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlist')
    anime = models.ForeignKey(AnimeList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Wishlist Entry"

    class Meta:
        unique_together = ('user', 'anime')