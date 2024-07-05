# Generated by Django 5.0.6 on 2024-07-04 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_gender_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(error_messages={'blank': '해당 닉네임이 이미 존재합니다.'}, max_length=50, unique=True),
        ),
    ]
