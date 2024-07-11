from django.urls import path
from .views import ProfileAPIView
from users import views

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user_list_create'),
    path('<int:id>/', views.UserDetailAPIView.as_view(), name='user_detail'),
    path('search/', views.UserNicknameSearchAPIView.as_view(), name='user_nickname_search'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('achievements_profile/', views.AchievementListAPIView.as_view(), name='achievements_profile'),
    path('login/',views.LoginAPIView.as_view(), name='login_api_view'),
    path('follow/<int:id>/',views.FollowAPIView.as_view(), name='follow_api_view'),
    path('followers/<int:id>/', views.UserFollowersAPIView.as_view(), name='user_followers_list_api_view'),
    path('following/<int:id>/', views.UserFollowingAPIView.as_view(), name='user_following_list_api_view'),

]