from rest_framework import serializers
from .models import *
from django.db.models import Q
from datetime import datetime

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'kakao_id',
            'password',
        ]

class EmailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]

class KakaoLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'kakao_id'
        ]

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ChangeLoginProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password',
            'email',
            'kakao_id',
        ]

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password',
        ]

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = [
            'user',
            'emoji'
        ]

class ProfileConciseSerializer(serializers.ModelSerializer):
    
    tedoori = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'username',
            'profile_pic',
            'tedoori',
        ]

    def get_tedoori(self, obj):
        todos_for_today = obj.user.todos.filter(date=datetime.today().strftime('%Y-%m-%d'))
        return todos_for_today.exists() and todos_for_today.filter(is_completed=True).count() == todos_for_today.count()

class CommentSerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    tedoori = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at_iso',
            'user',
            'username',
            'profile_pic',
            'tedoori',
            'description',
            'likes',
        ]
    
    def get_username(self, obj):
        profile = Profile.objects.get(user_id=obj.user.id)
        return profile.username
    
    def get_profile_pic(self, obj):
        try:
            profile = Profile.objects.get(user_id=obj.user.id)
            return profile.profile_pic.url if profile.profile_pic else None
        except FileNotFoundError:
            return None
        
    def get_tedoori(self, obj):
        todos_for_today = obj.user.todos.filter(date=datetime.today().strftime('%Y-%m-%d'))
        return todos_for_today.exists() and todos_for_today.filter(is_completed=True).count() == todos_for_today.count()

class CommentEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = [
            'description',
        ]

class TodoSerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    color = serializers.SerializerMethodField()
    
    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'color', 
            'description',
            'reminder',
            'reminder_iso',
            'created_at_iso',
            'date',
            'is_completed',
            'likes',
            'goal',
            'image'
        ]
        read_only_fields = [
            'created_by',
            'goal',
        ]
    
    def get_color(self, obj):
        color = obj.goal.color
        return color
    

class TodoDetailSerializer(serializers.ModelSerializer):
    
    likes = LikeSerializer(many=True, read_only=True)
    color = serializers.SerializerMethodField()
    
    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'color', 
            'description',
            'reminder',
            'reminder_iso',
            'date',
            'is_completed',
            'goal',
            'likes',
            'image',
        ]
        read_only_fields = [
            'goal',
            'created_by',
            'created_at_iso',
        ]
    
    def get_color(self, obj):
        color = obj.goal.color
        return color
    
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)

        if self.instance and self.instance.is_completed:
            fields['image'].read_only = False
        else:
            fields['image'].read_only = True

        return fields

class GoalSerializer(serializers.ModelSerializer):

    todos = serializers.SerializerMethodField()

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
        
    def get_todos(self, obj):
        todo_queryset = obj.todos.all()
        date_param = self.context.get('date')
        if date_param.lower() == 'null':
            todos_serializer = TodoSerializer(todo_queryset.filter(date=None), many=True)
            return todos_serializer.data
        else:
            try:
                date = datetime.strptime(date_param, '%Y-%m-%d')
                todos_serializer = TodoSerializer(todo_queryset.filter(date=date), many=True)
                return todos_serializer.data
            except:
                todos_serializer = TodoSerializer(todo_queryset, many=True)
                return todos_serializer.data

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

    tedoori = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ProfileSerializer, self).to_representation(instance)
        representation['follower_count'] = instance.user.followers.count()
        representation['following_count'] = instance.user.following.count()

        return representation
    
    def get_tedoori(self, obj):
        todos_for_today = obj.user.todos.filter(date=datetime.today().strftime('%Y-%m-%d'))
        return todos_for_today.exists() and todos_for_today.filter(is_completed=True).count() == todos_for_today.count()
    
class ProfileSearchAndAllSerializer(serializers.ModelSerializer):

    tedoori = serializers.SerializerMethodField()

    goal_colors = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ProfileSearchAndAllSerializer, self).to_representation(instance)
        representation['follower_count'] = instance.user.followers.count()
        representation['following_count'] = instance.user.following.count()

        return representation
    
    def get_tedoori(self, obj):
        todos_for_today = obj.user.todos.filter(date=datetime.today().strftime('%Y-%m-%d'))
        return todos_for_today.exists() and todos_for_today.filter(is_completed=True).count() == todos_for_today.count()
    
    def get_goal_colors(self, obj):
        goal_colors = []
        goals = obj.user.goals.filter(visibility='PB').order_by('created_at')[:4]
        for goal in goals:
            goal_colors.append(goal.color)
        return goal_colors
    
class ProfileTodoSerializer(serializers.ModelSerializer):

    tedoori = serializers.SerializerMethodField()

    todos = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'intro', 'profile_pic', 'todos', 'tedoori']

    def get_todos(self, obj):
        todos = obj.user.todos.filter(Q(is_completed=True) & Q(goal__visibility='PB')).order_by('created_at')[:5]
        return TodoSerializer(todos, many=True).data
    
    def get_tedoori(self, obj):
        todos_for_today = obj.user.todos.filter(date=datetime.today().strftime('%Y-%m-%d'))
        return todos_for_today.exists() and todos_for_today.filter(is_completed=True).count() == todos_for_today.count()

class ProfileTodoSearchSerializer(serializers.ModelSerializer):

    tedoori = serializers.SerializerMethodField()

    todos = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'intro', 'profile_pic', 'todos', 'tedoori']

    def get_todos(self, obj):
        keyword = self.context.get('title', '')
        todos = obj.user.todos.filter(Q(goal__visibility='PB') & Q(title__icontains=keyword)).order_by('created_at')
        return TodoSerializer(todos, many=True).data    
    
    def get_tedoori(self, obj):
        todos_for_today = obj.user.todos.filter(date=datetime.today().strftime('%Y-%m-%d'))
        return todos_for_today.exists() and todos_for_today.filter(is_completed=True).count() == todos_for_today.count()

        