# Generated by Django 5.0.6 on 2024-07-04 08:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_age_alter_user_email_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(blank=True, error_messages={'blank': '나이을 설정하시오'}, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, error_messages={'blank': '이메일을 입력하시오', 'unique': '해당 이메일이 이미 존재합니다.'}, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('남자', '남자(Man)'), ('여자', '여자(Woman)')], default='', error_messages={'blank': '성별을 선택하시오'}, max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, error_messages={'blank': '닉네임을 입력하시오', 'unique': '해당 닉네임이 이미 존재합니다.'}, max_length=50, unique=True),
        ),
    ]
