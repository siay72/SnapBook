from rest_framework import serializers
from .models import Post, Comment


class EmptySerializer(serializers.Serializer):
    pass


class CommentSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user_email', 'created_at']

class PostSerializer(serializers.ModelSerializer):

    total_likes = serializers.SerializerMethodField() 
    total_unlike = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user_email',
            'caption',
            'image',
            'video_url',
            'created_at',
            'total_likes',
            'total_unlike',
            'comments'
        ]

    def get_total_likes(self, obj):
        return obj.likes.count()
    
    def get_total_unlike(self, obj):
        return obj.unlikes.count()
    
