from django.db import models
from users.models import User
from config import settings

class Post(models.Model):
    COLOR_CHOICES = (
        ('빨강', '빨강(Red)'),
        ('주황', '주황(Orange)'),
        ('노랑', '노랑(Yellow)'), 
        ('초록', '초록(Green)'),
        ('파랑', '파랑(Blue)'), 
        ('보라', '보라(Purple)'),
    )

    title = models.CharField(max_length=50, null=True)
    content = models.TextField(max_length=1000, null=True, blank=True)
    comment = models.TextField(max_length=100, null=True)
    image = models.ImageField(upload_to='posts', null=True)
    color = models.CharField(max_length=2, choices=COLOR_CHOICES, default="")

    date = models.DateField(null=True) # 날짜 기입
    created_at = models.DateTimeField(auto_now_add=True) # 생성시간
    updated_at = models.DateTimeField(auto_now=True) # 수정시간

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
