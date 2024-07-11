import os
from rest_framework.response import Response
from users.models import User
from posts.models import Post
from users.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from achievements.models import Achievement
from user_achievements.models import UserAchievement
from user_achievements.serializers import UserAchievementSerializer

class AchievementListAPIView(ListAPIView):
    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # 기본 업적을 사용자에게 귀속
        for achievement in Achievement.objects.all():
            if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
                UserAchievement.objects.create(user=user, achievement=achievement, unlocked=False)

        # 사용자 업적 가져오기
        achievements = UserAchievement.objects.filter(user=user)

        # 업적 달성 조건 확인 및 상태 업데이트s
        for user_achievement in achievements:
            if not user_achievement.unlocked and self.check_achievement_unlocked(user, user_achievement.achievement, user_achievement.unlocked):
                user_achievement.unlocked = True
                user_achievement.save()
        return achievements
    def check_achievement_unlocked(self, user, achievement, unlocked):
        if unlocked:
            return True
        
        # 업적 달성 조건을 확인하는 로직 구현
        if achievement.title == '탐험의 시작' and user.followings.count() >= 1:
            return True
        elif achievement.title == '연결의 열쇠' and user.followers.count() >= 1:
            return True
        elif achievement.title == '인기의 중심' and user.followers.count() >= 50:
            return True
        elif achievement.title == '축하의 순간' and user.followers.count() >= 100:
            return True
        elif achievement.title == '창작의 첫 걸음' and Post.objects.filter(user=user).count() >= 1:
            return True
        elif achievement.title == '창작의 열정' and Post.objects.filter(user=user).count() >= 4:
            return True
        elif achievement.title == '창작의 반짝임' and Post.objects.filter(user=user).count() >= 8:
            return True

# 회원가입, 유저 전체 확인
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if len(response.data) == 0:
            return Response({"해당 유저가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        return response
    
# 특정 유저 찾기 - user_id를 통해서
class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(pk=kwargs['id'])
        except User.DoesNotExist:
            return Response({'해당 유저가 존재하지 않습니다'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
# 특정 유저 찾기 - nickname을 통해서
class UserNicknameSearchAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['nickname']

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if len(response.data) == 0:
            return Response({"해당 유저가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        return response

# 내 프로필 보기, 수정 및 삭제
class ProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_object(self):
        return self.request.user
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"해당 유저 정보를 삭제하였습니다."}, status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        if instance.profile_image:
            image_path = instance.profile_image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        # 유저 정보 삭제
        instance.delete()

    def perform_update(self, serializer):
        instance = serializer.instance
        # 기존 프로필 이미지를 삭제하는 경우
        if 'profile_image' in serializer.validated_data and not serializer.validated_data['profile_image']:
            if instance.profile_image:
                image_path = instance.profile_image.path
                if os.path.isfile(image_path):
                    os.remove(image_path)
            instance.profile_image = None

        serializer.save()

# 로그인
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'잘못된 아이디 혹은 비밀번호입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not check_password(password, user.password):
            return Response({'잘못된 아이디 혹은 비밀번호입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'token': str(token.access_token),
                'user': serializer.data,
            }
        )

#팔로우 
class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        user =request.user
        user_to_follow = get_object_or_404(User, id=id)
        if user == user_to_follow:
            return Response({"본인입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.followings.filter(id=id).exists():
            user.followings.remove(user_to_follow)
            return Response({'팔로우 취소했습니다'}, status=status.HTTP_200_OK)
        else:
            user.followings.add(user_to_follow)
            return Response({'팔로우 했습니다.'}, status=status.HTTP_200_OK)
        
#팔로우 리스트 확인
class UserFollowersAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['id'])
        return user.followers.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({'팔로워중인 유저가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#팔로잉 리스트 확인
class UserFollowingAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['id'])
        return user.followings.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({'팔로잉중인 유저가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

