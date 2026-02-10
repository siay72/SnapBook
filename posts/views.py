from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from posts.models import Post,  Comment
from posts.serializers import PostSerializer, CommentSerializer, EmptySerializer
from rest_framework import serializers
from posts.permissions import IsCommentAuthorOrReadOnly
from rest_framework.filters import SearchFilter
from posts.paginations import DefaultPagination
from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [SearchFilter]
    search_fields = ['caption', 'user__email']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()\
            .select_related('user')\
            .prefetch_related(
                'likes',
                'unlikes',
                Prefetch('comments', queryset=Comment.objects.select_related('user'))
            )\
            .order_by('-created_at')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_summary="Retrieve list of posts",
        operation_description="Public API to view all posts with pagination, search and filtering support.",
        responses={200: PostSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """Retrieve all posts"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a single post",
        responses={200: PostSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific post"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="Authenticated users can create posts with image or video URL.",
        request_body=PostSerializer,
        responses={
            201: PostSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Create post (Authenticated users only)"""
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Update a post",
        operation_description="Only post owner or admin can update the post.",
        request_body=PostSerializer,
        responses={
            200: PostSerializer,
            403: "Permission Denied"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        post = self.get_object()

        if not (self.request.user.is_staff or self.request.user.is_superuser):
            if post.user != self.request.user:
                raise serializers.ValidationError("You do not have permission to edit this post.")

        serializer.save()

    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="Only owner or admin can delete the post.",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Like a post",
        operation_description="Authenticated user can like a post.",
        responses={
            200: openapi.Response(
                description="Post liked successfully"
            )
        }
    )
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        post.unlikes.remove(user)
        post.likes.add(user)

        return Response({
            "message": "Post liked successfully.",
            "total_likes": post.likes.count(),
            "total_unlikes": post.unlikes.count(),
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Unlike a post",
        operation_description="Authenticated user can unlike a post.",
        responses={
            200: openapi.Response(
                description="Post unliked successfully"
            )
        }
    )
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        post.likes.remove(user)
        post.unlikes.add(user)

        return Response({
            "message": "Post unliked successfully.",
            "total_likes": post.likes.count(),
            "total_unlikes": post.unlikes.count()
        }, status=status.HTTP_200_OK)




class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs.get('post_pk')
        ).select_related('user')

    def get_serializer_context(self):
        return {
            'post_id': self.kwargs.get('post_pk')
        }

    @swagger_auto_schema(
        operation_summary="Retrieve all comments for a post",
        operation_description="Get all comments belonging to a specific post.",
        responses={200: CommentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List comments of a specific post"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a single comment",
        responses={200: CommentSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single comment of a post"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a comment",
        operation_description="Authenticated users can add comments to a post.",
        request_body=CommentSerializer,
        responses={
            201: CommentSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Create comment on a post"""
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            post_id=self.kwargs.get('post_pk')
        )

    @swagger_auto_schema(
        operation_summary="Update a comment",
        operation_description="Only comment owner can update the comment.",
        request_body=CommentSerializer,
        responses={
            200: CommentSerializer,
            403: "Permission Denied"
        }
    )
    def update(self, request, *args, **kwargs):
        """Update comment (owner only)"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a comment",
        operation_description="Only comment owner can delete the comment.",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete comment (owner only)"""
        return super().destroy(request, *args, **kwargs)

    


class MyPostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)\
            .select_related('user')\
            .prefetch_related('likes', 'unlikes', 'comments')\
            .order_by('-created_at')

    @swagger_auto_schema(
        operation_summary="Retrieve logged-in user posts",
        operation_description="Return all posts created by the currently authenticated user.",
        responses={200: PostSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """Get all posts of the logged-in user"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve single user post",
        responses={200: PostSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve one post of logged-in user"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="Authenticated user can create a post with text, image or video URL.",
        request_body=PostSerializer,
        responses={
            201: PostSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Create a new post for logged-in user"""
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Update own post",
        request_body=PostSerializer,
        responses={
            200: PostSerializer,
            403: "Permission Denied"
        }
    )
    def update(self, request, *args, **kwargs):
        """Update only your own post"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete own post",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete only your own post"""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Like your own post",
        operation_description="User can like a post they own.",
        responses={
            200: openapi.Response(
                description="Like response",
                examples={
                    "application/json": {
                        "message": "Post liked successfully.",
                        "total_likes": 10,
                        "total_unlikes": 2
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'], serializer_class=EmptySerializer)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        post.unlikes.remove(user)
        post.likes.add(user)

        return Response({
            "message": "Post liked successfully.",
            "total_likes": post.likes.count(),
            "total_unlikes": post.unlikes.count(),
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Unlike your own post",
        operation_description="User can unlike a post they own.",
        responses={
            200: openapi.Response(
                description="Unlike response",
                examples={
                    "application/json": {
                        "message": "Post unliked successfully.",
                        "total_likes": 8,
                        "total_unlikes": 3
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'], serializer_class=EmptySerializer)
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        post.likes.remove(user)
        post.unlikes.add(user)

        return Response({
            "message": "Post unliked successfully.",
            "total_likes": post.likes.count(),
            "total_unlikes": post.unlikes.count()
        }, status=status.HTTP_200_OK)