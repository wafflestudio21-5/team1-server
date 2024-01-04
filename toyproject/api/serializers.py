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

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'title', 
            'visibility',
        ]

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = [
            'description',
            'visibility',
            'mood',
        ]