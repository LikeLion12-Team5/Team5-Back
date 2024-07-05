# Generated by Django 5.0.6 on 2024-07-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('남자', '남자(Man)'), ('여자', '여자(Woman)')], default='남자', max_length=2),
        ),
    ]
