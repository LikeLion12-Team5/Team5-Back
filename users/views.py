import os
from rest_framework.response import Response
from users.models import User
from posts.models import Post
from users.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from achievements.models import Achievement
from user_achievements.models import UserAchievement
from user_achievements.serializers import UserAchievementSerializer
from django.db.models import Count, Sum
from posts.views import MostLikedPostsView
from datetime import timedelta
from django.utils import timezone
from datetime import datetime, date

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
    
    def get_achievement_progress(self, user, achievement):
        if achievement.title == '탐험의 시작':
            return user.followings.count()
        elif achievement.title == '연결의 열쇠':
            return user.followers.count()
        elif achievement.title == '인기의 중심':
            return user.followers.count()
        elif achievement.title == '축하의 순간':
            return user.followers.count()
        elif achievement.title == '창작의 첫 걸음':
            return Post.objects.filter(user=user).count()
        elif achievement.title == '창작의 열정':
            return Post.objects.filter(user=user).count()
        elif achievement.title == '창작의 반짝임':
            return Post.objects.filter(user=user).count()
        elif achievement.title == '공감의 새싹':
            return Post.objects.filter(user=user).aggregate(total_likes=Count('like_users'))['total_likes']
        elif achievement.title == '공감의 행운':
            return Post.objects.filter(user=user).aggregate(total_likes=Count('like_users'))['total_likes']
        elif achievement.title == '공감의 만개':
            return Post.objects.filter(user=user).aggregate(total_likes=Count('like_users'))['total_likes']
        elif achievement.title == '창작의 팔레트':
            return Post.objects.filter(user=user).values('color').distinct().count()
        return 0

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
        elif achievement.title == '공감의 새싹' and Post.objects.filter(like_users=user): # 공감 수 10개
            total_likes = Post.objects.filter(user=user).aggregate(total_likes=Count('like_users'))['total_likes']
            if total_likes >= 10:
                return True
        elif achievement.title == '공감의 행운': # 공감 수 50개
            total_likes = Post.objects.filter(user=user).aggregate(total_likes=Count('like_users'))['total_likes']
            if total_likes >= 50:
                return True
        elif achievement.title == '공감의 만개': # 공감 수 100개
            total_likes = Post.objects.filter(user=user).aggregate(total_likes=Count('like_users'))['total_likes']
            if total_likes >= 100:
                return True
        elif achievement.title == '창작의 팔레트': # 주간지 모든 색상 1회 이상 발행
            color_count = Post.objects.filter(user=user).values('color').distinct().count()
            if color_count == len(Post.COLOR_CHOICES):
                return True
        elif achievement.title == '영감을 주는 목소리':
            today = date.today()
            start_date = datetime.now() - timedelta(days=today.weekday() + 7)
            end_date = start_date + timedelta(days=6)
            top_post = Post.objects.filter(created_at__gte=start_date, created_at__lte=end_date)\
                                .annotate(num_likes=Count('like_users'))\
                                .order_by('-num_likes').first()
            if top_post and top_post.user == self.request.user:
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
                'access_token': str(token.access_token),
                'refresh_token': str(token),
                'user': serializer.data,
            }
        )
#리프레시 토큰에 따른 액세스 토큰 재발행
class RefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({'error': '리프레시 토큰이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            return Response({'error': '유효하지 않은 리프레시 토큰입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        new_access_token = str(refresh.access_token)
        return Response({'token': new_access_token}, status=status.HTTP_200_OK)
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

#상대가 나를 팔로우 했을 때, 취소하는 기능
class RemoveFollowerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        user_to_remove = get_object_or_404(User, id=id)
        
        if user == user_to_remove:
            return Response({"error": "본인입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user.followers.filter(id=id).exists():
            user_to_remove.followings.remove(user)
            return Response({'message': '상대방의 팔로우를 취소했습니다'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '상대방이 팔로우하고 있지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

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

