from django.urls import path
from achievements import views

urlpatterns = [
    path('', views.AchievementListAPIView.as_view(), name='achievements_profile'),
    
]