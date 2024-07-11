from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from posts.models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def comment_post_api_view(request, post_id):
    serializer = CommentSerializer(data=request.data)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def comment_list_api_view(request, post_id):
    comments = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH', 'DELETE'])
def comment_retrieve_api_view(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def comment_like_api_view(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=int(comment_id))
        
        if request.user.is_authenticated and comment.like_users.filter(id=request.user.id).exists():
            comment.like_users.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.is_authenticated:
            comment.like_users.add(request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)