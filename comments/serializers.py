from rest_framework import serializers
from comments.models import Comment
from users.serializers import UserSerializer
from posts.serializers import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    likes_num = serializers.SerializerMethodField()
    user = UserSerializer(required=False)
    post = PostSerializer(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'likes_num', 'user', 'post']
    
    # 가능하다면 likes_num도 추가해보기
    def get_likes_num(self, obj):
        return obj.like_users.count()