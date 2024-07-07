from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user_list_create'),
    path('<int:id>/', views.UserDetailAPIView.as_view(), name='user_detail'),
    path('search/', views.UserNicknameSearchAPIView.as_view(), name='user_nickname_search'),
    path('profile/', views.ProfileAPIView.as_view(), name='user_profile'),
    path('achievements_profile/', views.AchievementListAPIView.as_view(), name='achievements_profile'),
    path('login/',views.LoginAPIView.as_view(), name='login'),
    path('follow/<int:id>/',views.FollowAPIView.as_view(), name='follow_api_view'),
    path('followers/<int:id>/', views.UserFollowersAPIView.as_view(), name='user_followers_list'),
    path('following/<int:id>/', views.UserFollowingAPIView.as_view(), name='user_following_list'),
    

]