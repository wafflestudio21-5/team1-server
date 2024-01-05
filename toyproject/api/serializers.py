from rest_framework import serializers
from .models import *

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'title', 
            'description',
            'reminder',
            'start_date',
            'end_date',
        ]

class TodoConciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'title', 
            'reminder',
        ]

class GoalSerializer(serializers.ModelSerializer):

    todo_set = TodoConciseSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = [
            'title', 
            'visibility',
            'todo_set',
        ]

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = [
            'description',
            'visibility',
            'mood',
        ]