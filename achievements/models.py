from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def achievement_directory_path(instance, filename):
    # 파일을 'achievement_<id>/<filename>' 경로에 업로드합니다.
    return f'achievement_{instance.id}/{filename}'

class Achievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    explain = models.CharField(max_length=500)
    badge = models.ImageField(upload_to=achievement_directory_path, blank =True, null=True)
    default_locked = models.BooleanField(default=False)

