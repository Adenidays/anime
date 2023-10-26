from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from userapp.serializers import ChangePasswordSerializer, ChangeUsernameSerializer, ChangeEmailSerializer


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
