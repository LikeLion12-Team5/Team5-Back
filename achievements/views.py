# achievements/views.py
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Achievement
from .serializers import AchievementSerializer
from rest_framework.generics import ListAPIView

class AchievementListAPIView(ListAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 필요한 업적 리스트
        required_achievements = [
            {'title': '첫 친구!', 'explain': '팔로워 수가 1 이상일 경우', 'badge': None, 'default_locked': False},
            # 다른 업적도 여기에 추가할 수 있습니다.
        ]
        
        # 사용자가 이미 가지고 있는 업적 타이틀 리스트
        user_achievements = Achievement.objects.filter(user=user).values_list('title', flat=True)
        
        # 필요한 업적 중 사용자가 아직 가지고 있지 않은 업적 추가
        for achievement_data in required_achievements:
            if achievement_data['title'] not in user_achievements:
                Achievement.objects.create(user=user, **achievement_data)
        
        # 사용자 업적 가져오기
        achievements = Achievement.objects.filter(user=user)
        
        # 업적 달성 조건 확인 및 상태 업데이트
        for achievement in achievements:
            if not achievement.status and self.check_achievement_condition(user, achievement):
                achievement.status = True
                achievement.save()
        
        return achievements

    def check_achievement_condition(self, user, achievement):
        # 예: 팔로워 수가 1 이상일 경우 업적 달성
        if achievement.title == '첫 친구!' and user.followers.count() >= 1:
            return True
        return False
