from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .serializers import TodoSerializer, GoalSerializer, DiarySerializer, FollowRelationSerializer, TodoConciseSerializer, ProfileSerializer
from .models import Goal, Todo, Diary, User, Profile

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from django.http import Http404

from django.shortcuts import get_object_or_404

from datetime import datetime
    
class GoalListCreateAPIView(ListCreateAPIView):
    serializer_class = GoalSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Goal.objects.filter(created_by=user)


class GoalDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    lookup_url_kwarg = 'goal_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Goal.objects.filter(created_by=user)

class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoConciseSerializer

    def perform_create(self, serializer):
        goal_id = self.kwargs.get('goal_id')
        return serializer.save(created_by=self.request.user, goal=Goal.objects.get(id=goal_id))
    
    def get_queryset(self):
        goal_id = self.kwargs.get('goal_id')
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Todo.objects.filter(created_by=user, goal=Goal.objects.get(id=goal_id))
    
class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    lookup_url_kwarg = 'todo_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Todo.objects.filter(created_by=user)

class DiaryCreateAPIView(CreateAPIView):
    serializer_class = DiarySerializer

    def perform_create(self, serializer):
        if self.request.user is User:
            return serializer.save(created_by=self.request.user)
        else:
            return serializer.save(created_by=User.objects.get(id=3))
    
class DiaryListAPIView(ListAPIView):
    serializer_class = DiarySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Diary.objects.filter(created_by=User.objects.get(id=user_id))
    
class DiaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DiarySerializer

    def get_object(self):
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        obj = Diary.objects.get(created_by_id=self.kwargs['user_id'], date=date)
        return obj

    
class FollowRelationAPIView(RetrieveAPIView):
    serializer_class = FollowRelationSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'

class ProfileDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'user_id'
    


