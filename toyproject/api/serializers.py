from rest_framework import serializers
from .models import *
from django.db.models import Q

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]

class SignUpKakaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'kakao_id',
        ]

class EmailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]

class KakaoLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'kakao_id',
        ]

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = [
            'user',
            'emoji'
        ]

class CommentSerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at_iso',
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
            'created_by',
            'description',
            'reminder_iso',
            'created_at_iso',
            'date',
            'is_completed',
            'goal',
            'likes',
        ]

class TodoConciseSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    color = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        fields = [
            'id',
            'title', 
            'color',
            'description',
            'reminder_iso',
            'created_at_iso',
            'date',
            'is_completed',
            'likes',
        ]

    def get_color(self, obj):
        color = obj.goal.color
        return color

class GoalSerializer(serializers.ModelSerializer):

    todos = TodoConciseSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = [
            'id',
            'title', 
            'visibility',
            'color',
            'created_at_iso',
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
            'color',
            'emoji',
            'image',
            'created_by',
            'date',
            'likes',
            'comments',
        ]

class ProfileConciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'username'
        ]

class FollowSerializer(serializers.ModelSerializer):
    
    profile = ProfileConciseSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'profile',
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

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ProfileSerializer, self).to_representation(instance)
        representation['follower_count'] = instance.user.followers.count()
        representation['following_count'] = instance.user.following.count()

        return representation
    
class ProfileTodoSerializer(serializers.ModelSerializer):

    todos = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'intro', 'profile_pic', 'todos']

    def get_todos(self, obj):
        todos = obj.user.todos.filter(Q(is_completed=True) & Q(goal__visibility='PB')).order_by('created_at')[:5]
        return TodoConciseSerializer(todos, many=True).data

class ProfileTodoSearchSerializer(serializers.ModelSerializer):

    todos = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'intro', 'profile_pic', 'todos']

    def get_todos(self, obj):
        keyword = self.context.get('title', '')
        todos = obj.user.todos.filter(Q(goal__visibility='PB') & Q(title__icontains=keyword)).order_by('created_at')[:5]
        return TodoConciseSerializer(todos, many=True).data    