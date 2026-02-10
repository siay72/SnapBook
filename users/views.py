from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserProfileSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # User can only access his own profile
        return User.objects.filter(id=self.request.user.id)

    @swagger_auto_schema(
        operation_summary="Get current user profile",
        operation_description="Retrieve the profile information of the currently logged-in user.",
        responses={200: UserProfileSerializer}
    )
    def list(self, request, *args, **kwargs):
        """Return profile data of authenticated user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="Authenticated user can update their profile details like phone, location etc.",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: "Bad Request"
        }
    )
    def update(self, request, *args, **kwargs):
        """Update profile details"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update user profile",
        operation_description="Partially update profile fields.",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update profile"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None
    )
    def create(self, request, *args, **kwargs):
        """Disable POST method"""
        return Response(
            {"detail": "Method 'POST' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @swagger_auto_schema(
        auto_schema=None
    )
    def destroy(self, request, *args, **kwargs):
        """Disable DELETE method"""
        return Response(
            {"detail": "Method 'DELETE' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )