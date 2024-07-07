# Generated by Django 5.0.6 on 2024-07-06 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='explain',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='title',
            field=models.CharField(default='기본 설명', max_length=50),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='unlock_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
