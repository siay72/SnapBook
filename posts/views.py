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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()

        if not (self.request.user.is_staff or self.request.user.is_superuser):
            if post.user != self.request.user:
                raise serializers.ValidationError("You do not have permission to edit this post.")

        serializer.save()


    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            if instance.user != self.request.user:
                raise serializers.ValidationError("You do not have permission to delete this post.")

        instance.delete()

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




class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()\
        .select_related('user')\
        .prefetch_related(
            'likes',
            'unlikes',
            Prefetch('comments', queryset=Comment.objects.select_related('user'))
        )\
        .order_by('-created_at')


    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs.get('post_pk')
        ).select_related('user')

    def get_serializer_context(self):
        return {'post_id': self.kwargs.get('post_pk')     }
    


class MyPostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)\
            .select_related('user')\
            .prefetch_related('likes', 'unlikes', 'comments')\
            .order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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