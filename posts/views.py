from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from posts.permissions import IsOwner, OnlyRead
from rest_framework.permissions import IsAuthenticated
import logging


# 검색(전체), 검색(post_id), 검색(color) 게시, 수정, 삭제
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    ordering = '-id'
    permission_classes = [IsOwner|OnlyRead]
    filter_backends = [filters.SearchFilter]
    search_fields = ['color']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 좋아요
@api_view(['POST'])
def post_like_api_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.like_users.filter(id=request.user.id).exists():
        post.like_users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        post.like_users.add(request.user)
        return Response(status=status.HTTP_201_CREATED)
    
# 유저 검색
# class MyPostAPIView(ListAPIView):
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['color']
#     def get(self, request):
#         try:
#             post_set = Post.objects.filter(user=request.user)
#             post_list = [{"id": post.id,
#                           "title": post.title,
#                           "content": post.content,
#                           "comment": post.comment,
#                           }for post in post_set]
#             return Response({"result": post_list}, status=status.HTTP_200_OK)
#         except KeyError:
#             return Response({"message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

class MyPostAPIView(ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['color']

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)