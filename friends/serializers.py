from rest_framework import serializers
from .models import FriendRequest, Friendship, Notification


class FriendRequestSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)
    receiver_email = serializers.EmailField(source="receiver.email", read_only=True)
    is_read = serializers.BooleanField(source="receiver.notifications.filter(reference_id=instance.id, notification_type='friend_request').first().is_read", read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'sender_email', 'receiver_email', 'is_read','status', 'created_at']
        read_only_fields = ("sender","is_read", "status")


class FriendshipSerializer(serializers.ModelSerializer):

    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']

    def get_friend(self, obj):
        request = self.context.get("request")

        if obj.user1 == request.user:
            user = obj.user2
        else:
            user = obj.user1

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }


class NotificationSerializer(serializers.ModelSerializer):

    sender_name = serializers.SerializerMethodField()
    sender_profile_picture = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "message",
            "request_status",
            "is_read",
            "created_at",
            "reference_id",
            "sender_name",
            "sender_profile_picture"
        ]

    def get_request_status(self, obj):
        if obj.notification_type == "friend_request" and obj.reference_id:
            try:
                fr = FriendRequest.objects.get(id=obj.reference_id)
                return fr.status   # pending / accepted / rejected
            except FriendRequest.DoesNotExist:
                return None
        return None

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    def get_sender_profile_picture(self, obj):
        try:
            if hasattr(obj.sender, "profile_picture") and obj.sender.profile_picture:
                return obj.sender.profile_picture.url
        except:
            pass
        return None