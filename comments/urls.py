from django.urls import path
from comments import views

urlpatterns = [
    path('post/<int:post_id>/', views.comment_post_api_view, name='comment-post'),
    path('get/<int:post_id>/', views.comment_list_api_view, name='comment-list'),
    path('edit/<int:comment_id>/', views.comment_retrieve_api_view, name='comment-edit'),
    path('like/<int:comment_id>/', views.comment_like_api_view, name='comment-like'),
]