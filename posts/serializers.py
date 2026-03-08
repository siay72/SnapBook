from rest_framework import serializers
from .models import Post, Comment
from decouple import config


class EmptySerializer(serializers.Serializer):
    pass


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'user_email',
            'user_id',
            'user_first_name',
            'user_last_name',
            'created_at'
        ]


# Post Serializer
class PostSerializer(serializers.ModelSerializer):

    user_profile_picture = serializers.SerializerMethodField()
    # Like / Unlike counters
    total_likes = serializers.SerializerMethodField()
    total_unlike = serializers.SerializerMethodField()

    # User activity state
    is_liked = serializers.SerializerMethodField()
    is_unliked = serializers.SerializerMethodField()

    # Comment counter
    total_comments = serializers.SerializerMethodField()

    image = serializers.ImageField(required=False)

    # User info
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)

    # Nested comments
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user_email',
            "user_profile_picture",
            'user_first_name',
            'user_last_name',
            'caption',
            'image',
            'video_url',
            'created_at',

            'total_likes',
            'total_unlike',
            'is_liked',
            'is_unliked',

            'total_comments',
            'comments'
        ]
    def get_user_profile_picture(self, obj):
        if obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None

    # Like count
    def get_total_likes(self, obj):
        return obj.likes.count()


    # Unlike count
    def get_total_unlike(self, obj):
        return obj.unlikes.count()


    # Comment count
    def get_total_comments(self, obj):
        return obj.comments.count()


    # Check if current user liked
    def get_is_liked(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()

        return False


    # Check if current user unliked
    def get_is_unliked(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.unlikes.filter(id=request.user.id).exists()

        return False