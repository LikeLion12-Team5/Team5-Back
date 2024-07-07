# migrations/0005_alter_achievement_expain_and_more.py

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def create_initial_achievements(apps, schema_editor):
    Achievement = apps.get_model('achievements', 'Achievement')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    
    for user in User.objects.all():
        Achievement.objects.create(
            user=user,
            title='첫 친구!',
            explain='팔로워 수가 1 이상일 경우',
            badge=None,
            default_locked=False
        )

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0005_alter_achievement_expain'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievement',
            name='expain',
        ),
        migrations.AddField(
            model_name='achievement',
            name='explain',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievement',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserAchievement',
        ),
        migrations.RunPython(create_initial_achievements),
    ]
