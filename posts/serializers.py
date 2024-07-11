from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    comments_num = serializers.SerializerMethodField()
    likes_num = serializers.SerializerMethodField()
    user = UserSerializer(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'comment', 'color', 'image', 'date', 'created_at', 'comments_num', 'likes_num', 'user']

    # 게시물의 댓글 개수
    def get_comments_num(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    # 가능하다면 likes_num도 추가해보기
    def get_likes_num(self, obj):
        return obj.like_users.count()
    