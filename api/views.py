from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .serializers import TodoSerializer, GoalSerializer, DiarySerializer, FollowRelationSerializer, TodoConciseSerializer
from .models import Goal, Todo, Diary, User

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from django.http import Http404
    
class GoalListCreateAPIView(ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Goal.objects.filter(created_by=user)

class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoConciseSerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Todo.objects.filter(created_by=user)

class DiaryCreateAPIView(CreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
    
class DiaryListAPIView(ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Diary.objects.filter(created_by=User.objects.get(id=user_id))
    
class DiaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    lookup_url_kwarg = 'diary_id'
    permission_classes = (IsAuthenticated,)
    
class FollowRelationAPIView(RetrieveAPIView):
    serializer_class = FollowRelationSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    permission_classes = (IsAuthenticated,)

