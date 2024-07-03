from rest_framework import serializers
from posts.models import Post
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    posts_num = serializers.SerializerMethodField()
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id','username', 'nickname', 'email', 'gender', 'age', 'profile_image', 'password', 'password_confirm', 'posts_num']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }

    # 유저의 포스트 개수
    def get_posts_num(self, obj):
        return Post.objects.filter(user=obj).count()
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다")
        return data
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user