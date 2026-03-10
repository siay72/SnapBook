from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from rest_framework.permissions import IsAdminUser
from users.serializers import UserProfileSerializer


class AdminUserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):

        user = self.get_object()

        if user == request.user:
            return Response(
                {"error": "You cannot delete yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()

        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_200_OK
        )





class UserProfileView(ModelViewSet):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @swagger_auto_schema(
        operation_summary="Get current user profile",
        operation_description="Retrieve the profile information of the currently logged-in user.",
        responses={200: UserProfileSerializer}
    )
    def list(self, request, *args, **kwargs):

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=UserProfileSerializer,
        consumes=["multipart/form-data"],
    )
    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Partial update profile",
        request_body=UserProfileSerializer,
        consumes=["multipart/form-data"],
    )
    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'POST' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'DELETE' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )