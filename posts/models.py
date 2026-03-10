from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    caption = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )
    unlikes = models.ManyToManyField(
        User,
        related_name='unliked_posts',
        blank=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.caption[:20]}"
    


class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text





class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order_id = models.CharField(max_length=100, unique=True)

    transaction_id = models.CharField(max_length=150)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=50)

    status = models.CharField(max_length=20, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.order_id}"