from django.db.models import F
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from userapp.models import WishList, AnimeCollection
from userapp.serializers import ChangePasswordSerializer, ChangeUsernameSerializer, ChangeEmailSerializer, \
    WishListSerializer, WishListCreateSerializer, AnimeCollectionSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            if not user.check_password(old_password):
                return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({"error": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password successfully changed"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            new_username = serializer.validated_data['new_username']

            user.username = new_username
            user.save()

            return Response({"message": "Username successfully changed"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeEmailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_email = serializer.validated_data['old_email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            new_email = serializer.validated_data['new_email']

            if (
                    user.email == old_email and
                    user.check_password(password) and
                    password == confirm_password
            ):
                user.email = new_email
                user.save()
                return Response({"message": "Email successfully changed"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email, password, or confirmation password"},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListView(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WishListCreateSerializer
        return WishListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserWishListView(generics.ListAPIView):
    serializer_class = WishListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return WishList.objects.filter(user_id=user_id)


class AnimeCollectionCreateView(generics.CreateAPIView):
    serializer_class = AnimeCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CollectionListView(generics.ListAPIView):
    serializer_class = AnimeCollectionSerializer

    def get_queryset(self):
        queryset = AnimeCollection.objects.all()

        if self.request.query_params.get('popular'):
            queryset = queryset.annotate(subscribers_count=F('subscribers')).order_by('-subscribers_count')

        return queryset.prefetch_related('anime')