from rest_framework import serializers
from .models import UserAchievement
from users.serializers import UserSerializer
from achievements.serializers import AchievementSerializer

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()
    user = UserSerializer()
    class Meta:
        model = UserAchievement
        fields = "__all__"

    def get_progress(self, obj):
        view = self.context['view']
        return view.get_achievement_progress(obj.user, obj.achievement)