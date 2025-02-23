from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:post_id>/', views.post_like_api_view, name='post-like'),
    path('getlike/<int:post_id>/', views.get_like_api_view, name='get-like'),
    path('my/', views.MyPostAPIView.as_view(), name='my-post'),
    path('mycolors/', views.MyColorsNumAPIView.as_view(), name='my-colors'),
    path('mostlike/', views.MostLikedPostsView.as_view(), name='most-like'),
    path('mostcolor/', views.MostFrequentColorView.as_view(), name='most-color'),
]