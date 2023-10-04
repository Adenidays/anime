from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

from animeapp.models import AnimeList


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        if not email:
            raise ValueError('The email is required to create this user')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_staff=False, is_active=True, is_superuser=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField("Email", unique=True)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    username = models.CharField("User Name", max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
    subscribers = models.PositiveIntegerField(default=0)
    anime = models.ManyToManyField(AnimeList)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(AnimeCollection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} подписан на {self.collection.name}"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlist')
    anime = models.ForeignKey(AnimeList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user_name}'s Wishlist Entry"

    class Meta:
        unique_together = ('user', 'anime')
