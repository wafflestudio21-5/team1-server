from rest_framework import serializers
from .models import *

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'user'
        ]

class CommentSerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'created_at',
            'user',
            'description',
            'likes',
        ]

class TodoSerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Todo
        fields = [
            'id',
            'title', 
            'description',
            'reminder',
            'created_at',
            'date',
            'is_completed',
            'goal',
            'likes',
        ]

class TodoConciseSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Todo
        fields = [
            'id',
            'title', 
            'description',
            'created_at',
            'date',
            'is_completed',
            'likes',
        ]

class GoalSerializer(serializers.ModelSerializer):

    todos = TodoConciseSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = [
            'id',
            'title', 
            'visibility',
            'color',
            'created_at',
            'todos',
        ]

class DiarySerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Diary
        fields = [
            'id',
            'description',
            'visibility',
            'mood',
            'image',
            'created_by',
            'date',
            'likes',
            'comments',
        ]

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]

class FollowRelationSerializer(serializers.ModelSerializer):
    
    following = FollowSerializer(many=True, read_only=True)
    followers = FollowSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'following',
            'followers',
        ]

