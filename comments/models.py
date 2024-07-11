from django.db import models
from users.models import User
from posts.models import Post
from config import settings

class Comment(models.Model):
    content = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')