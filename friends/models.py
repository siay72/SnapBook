from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.email} -> {self.receiver.email}"


class Friendship(models.Model):

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_2')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('friend_request', 'Friend Request'),
        ('friend_accept', 'Friend Accept'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    message = models.TextField(blank=True, null=True)

    is_read = models.BooleanField(default=False)

    reference_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)