from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from posts.models import Post,  Comment
from posts.serializers import PostSerializer, CommentSerializer, EmptySerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

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




class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post does not exist")

        serializer.save(
            post=post,
            user=self.request.user
        )
