from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db import models
from posts.serializers import EmptySerializer
from .models import FriendRequest, Friendship, Notification
from .serializers import FriendRequestSerializer, FriendshipSerializer, NotificationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequestViewSet(ModelViewSet):

    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(receiver=self.request.user)
        ).order_by("-created_at")

    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data["receiver"]

        if sender == receiver:
            raise serializers.ValidationError("Cannot send request to yourself")

        # already friends
        if Friendship.objects.filter(
            models.Q(user1=sender, user2=receiver) |
            models.Q(user1=receiver, user2=sender)
        ).exists():
            raise serializers.ValidationError("Already friends")

        # duplicate request
        if FriendRequest.objects.filter(
            sender=sender,
            receiver=receiver,
            status="pending"
        ).exists():
            raise serializers.ValidationError("Already sent")

        # SAVE FIRST
        friend_request = serializer.save(sender=sender)

        # CREATE NOTIFICATION
        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="friend_request",
            message="sent you a friend request",
            reference_id=friend_request.id
        )

    @action(detail=False, methods=["get"], url_path="status/(?P<user_id>[^/.]+)")
    def status(self, request, user_id=None):

        current_user = request.user

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        #  Check if already friends
        is_friend = Friendship.objects.filter(
            models.Q(user1=current_user, user2=target_user) |
            models.Q(user1=target_user, user2=current_user)
        ).exists()

        if is_friend:
            friendship = Friendship.objects.filter(
                models.Q(user1=current_user, user2=target_user) |
                models.Q(user1=target_user, user2=current_user)
            ).first()

            return Response({
                "status": "friends",
                "friendship_id": friendship.id  
    })

        #  Sent request
        sent_request = FriendRequest.objects.filter(
            sender=current_user,
            receiver=target_user,
            status="pending"
        ).exists()

        if sent_request:
            return Response({"status": "request_sent"})

        #  Received request
        received_request = FriendRequest.objects.filter(
            sender=target_user,
            receiver=current_user,
            status="pending"
        ).exists()

        if received_request:
            return Response({"status": "request_received"})

        return Response({"status": "none"})

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"error": "Not allowed"}, status=403)

        if friend_request.status != "pending":
            return Response({"error": "Already handled"}, status=400)

        friend_request.status = "accepted"
        friend_request.save()

        user1 = min(friend_request.sender, friend_request.receiver, key=lambda u: u.id)
        user2 = max(friend_request.sender, friend_request.receiver, key=lambda u: u.id)

        Friendship.objects.get_or_create(user1=user1, user2=user2)

        # UPDATE EXISTING NOTIFICATION
        Notification.objects.filter(
            receiver=request.user,
            reference_id=friend_request.id,
            notification_type="friend_request"
        ).update(is_read=True)

        return Response({"message": "Friend request accepted"})


    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.sender != request.user:
            return Response({"error": "Not allowed"}, status=403)

        if friend_request.status != "pending":
            return Response({"error": "Cannot cancel"}, status=400)

        # UPDATE NOTIFICATION BEFORE DELETE
        Notification.objects.filter(
            receiver=friend_request.receiver,
            reference_id=friend_request.id,
            notification_type="friend_request"
        ).update(is_read=True)

        friend_request.delete()

        return Response({"message": "Friend request cancelled"})
        

class FriendshipViewSet(ModelViewSet):

    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            models.Q(user1=self.request.user) |
            models.Q(user2=self.request.user)
        )

    def get_serializer_context(self):
        return {"request": self.request}
    
    @action(detail=True, methods=["post"])
    def unfriend(self, request, pk=None):
        friendship = self.get_object()

        if request.user not in [friendship.user1, friendship.user2]:
            return Response({"error": "Not allowed"}, status=403)

        friendship.delete()
        return Response({"message": "Unfriended successfully"})


class NotificationViewSet(ReadOnlyModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            receiver=self.request.user
        ).order_by("-created_at")

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"message": "Marked as read"})

    # DELETE NOTIFICATION
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        notification = self.get_object()
        notification.delete()
        return Response({"message": "Notification deleted"})