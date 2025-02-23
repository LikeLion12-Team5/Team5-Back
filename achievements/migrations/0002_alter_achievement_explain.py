# Generated by Django 5.0.6 on 2024-07-08 06:06

from django.db import migrations, models

def create_default_achievements(apps, schema_editor):
    Achievement = apps.get_model('achievements', 'Achievement')
    default_achievements = [
        {'title': '탐험의 시작', 'explain': '첫 팔로잉시 부여'},
        {'title': '연결의 열쇠', 'explain': '첫 팔로워 달성시 부여'},
        {'title': '인기의 중심', 'explain': '팔로워 50명 달성시 부여'},
        {'title': '축하의 순간', 'explain': '팔로워 100명 달성시 부여'},
        {'title': '창작의 첫 걸음', 'explain': '주간지 첫 발행시 부여'},
        {'title': '창작의 열정', 'explain': '주간지 4회 이상 발행시 부여'},
        {'title': '창작의 반짝임', 'explain': '주간지 8회 이상 발행시 부여'},
        {'title': '창작의 팔레트', 'explain': '모든 색깔 1회 이상 발행시 부여'},
        {'title': '공감의 새싹', 'explain': '공감수 10개 이상 달성시 부여'},
        {'title': '공감의 행운', 'explain': '공감수 50개 이상 달성시 부여'},
        {'title': '공감의 만개', 'explain': '공감수 100개 이상 달성시 부여'},
        {'title': '영감을 주는 목소리', 'explain': '대표 코멘트 선정시 부여'},
    ]
    for achievement in default_achievements:
        Achievement.objects.create(**achievement)


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
        migrations.RunPython(create_default_achievements),
    ]
