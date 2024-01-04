from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .serializers import TodoSerializer, GoalSerializer, DiarySerializer
from .models import Goal, Todo, Diary
    
class GoalListCreateAPIView(ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        return Goal.objects.filter(created_by=self.request.user)

class GoalDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    lookup_url_kwarg = 'goal_id'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Goal.objects.filter(created_by=self.request.user)

class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        goal_id = self.kwargs.get('goal_id')
        return serializer.save(created_by=self.request.user, goal=Goal.objects.get(id=goal_id))
    
    def get_queryset(self):
        goal_id = self.kwargs.get('goal_id')
        return Todo.objects.filter(created_by=self.request.user, goal=Goal.objects.get(id=goal_id))
    
class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    lookup_url_kwarg = 'todo_id'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Todo.objects.filter(created_by=self.request.user)

class DiaryCreateAPIView(CreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
    
class DiaryListAPIView(ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Diary.objects.filter(created_by=self.request.user)
    
class DiaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DiarySerializer
    lookup_url_kwarg = 'diary_id'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Diary.objects.filter(created_by=self.request.user)