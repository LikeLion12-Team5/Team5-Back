from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.db.models import Count
from rest_framework.views import APIView
from posts.permissions import IsOwner, OnlyRead
from rest_framework.permissions import IsAuthenticated


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
        return Response({"공감을 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)
    else:
        post.like_users.add(request.user)
        return Response({"공감을 눌렀습니다."}, status=status.HTTP_201_CREATED)
    
# 좋아요
@api_view(['POST'])
def get_like_api_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.like_users.filter(id=request.user.id).exists():
        return Response({True}, status=status.HTTP_200_OK)
    else:
        return Response({False}, status=status.HTTP_200_OK)
    
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


# 자신의 색깔별 게시글 수 검색
class MyColorsNumAPIView(APIView):
    def get(self, request):
        try:
            # 현재 로그인한 사용자의 게시물 필터링
            post_set = Post.objects.filter(user=request.user)
            
            # 각 색상별 게시물 수를 주석으로 추가
            color_counts = post_set.values('color').annotate(count=Count('color'))

            # 모든 색상 선택지를 0으로 설정하여 색상 맵 초기화
            color_map = {color_choice[0]: 0 for color_choice in Post.COLOR_CHOICES}

            # 쿼리에서 실제 카운트로 color_map 업데이트
            for item in color_counts:
                color_map[item['color']] = item['count']

            # 색상 코드를 한글 이름으로 변환
            post_list = {color_choice[0]: color_map[color_choice[0]] for color_choice in Post.COLOR_CHOICES}

            return Response({"result": post_list}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
        

# 자신의 색깔별 게시글 수 검색
class ColorsNumAPIView(ListAPIView):
    def get_queryset(self):
        return Post.objects.filter(like_users=self.request.user)