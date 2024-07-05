from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

def user_directory_path(instance, filename):
    # 파일을 'user_<id>/<filename>' 경로에 업로드합니다.
    return f'user_{instance.id}/{filename}'

class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, error_messages={
            "unique": ("해당 닉네임이 이미 존재합니다."),
        },)
    email = models.EmailField(max_length = 254, unique=True, error_messages={
            "unique": ("해당 이메일이 이미 존재합니다."),
        },)
    GENDER_CHOICES = (
        ('남자', '남자(Man)'),
        ('여자', '여자(Woman)'),
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="남자")
    sign_up_at = models.DateTimeField(auto_now_add=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    profile_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    