from django.urls import path
from .views import ProfileAPIView
from users import views

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user_list_create'),
    path('<int:id>/', views.UserDetailAPIView.as_view(), name='user_detail'),
    path('search/', views.UserNicknameSearchAPIView.as_view(), name='user_nickname_search'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('login/',views.LoginAPIView.as_view(), name='login_api_view'),

]