from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from .serializers import (  TodoSerializer, 
                            GoalSerializer, 
                            DiarySerializer, 
                            FollowRelationSerializer, 
                            TodoConciseSerializer, 
                            ProfileSerializer,
                            SignUpKakaoSerializer,
                            SignUpSerializer,
                            EmailLoginSerializer,
                            KakaoLoginSerializer,
                        )
from .models import Goal, Todo, Diary, User, Profile

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from django.http import Http404

from django.shortcuts import get_object_or_404

from django.db.models import Q

from datetime import datetime

from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 3

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)

class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                return Response({
                    "result_code" : 1,
                    "result" : "FAIL",
                    "error_msg" : "User with this email already exists",
                    "token" : Token.objects.get(user=user).key,
                    "user_id" : ""
                }, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                user = serializer.save()
                return Response({
                    "result_code" : 0,
                    "result" : "SUCCESS",
                    "error_msg" : "",
                    "token" : Token.objects.get(user=user).key,
                    "user_id" : user.id
                }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors[0],
            "token" : "",
            "user_id" : ""
        }, status=status.HTTP_400_BAD_REQUEST)


class SignUpKakaoAPIView(CreateAPIView):
    serializer_class = SignUpKakaoSerializer

    def post(self, request, *args, **kwargs):
        serializer = SignUpKakaoSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "result_code" : 0,
                "result" : "SUCCESS",
                "error_msg" : "",
                "token" : Token.objects.get(user=user).key,
                "kakao_id" : user.kakao_id,
                "user_id" : user.id
            }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors[0],
            "token" : "",
            "kakao_id" : "",
            "user_id" : ""
        }, status=status.HTTP_400_BAD_REQUEST)


class SignupGuestAPIView(RetrieveAPIView): # need to review...
    def get(self, request, *args, **kwargs):
        user = User.objects.create()
        return Response({
            "token": Token.objects.get(user=user).key,
            "user_id": user.id
        }, status=status.HTTP_200_OK)

class LoginEmailAPIView(CreateAPIView):
    serializer_class = EmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailLoginSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except ObjectDoesNotExist:
                return Response({
                    "result_code" : 1,
                    "result" : "FAIL",
                    "error_msg" : "User does not exist",
                    "token" : ""
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "result_code" : 0,
                "result" : "SUCCESS",
                "error_msg" : "",
                "token" : Token.objects.get(user=user).key
            }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors[0],
            "token" : ""
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginKakaoAPIView(CreateAPIView):
    serializer_class = KakaoLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = KakaoLoginSerializer(data=request.data)
        if serializer.is_valid():
            try: 
                user = User.objects.get(kakao_id=serializer.validated_data['kakao_id'])
            except ObjectDoesNotExist:
                return Response({
                    "result_code" : 2,
                    "result" : "FAIL",
                    "error_msg" : "KaKao User needs to sign up",
                    "token" : ""
                }, status=status.HTTP_200_OK)
            return Response({
                "result_code" : 0,
                "result" : "SUCCESS",
                "error_msg" : "",
                "token" : Token.objects.get(user=user).key
            }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors,
            "token" : ""
        }, status=status.HTTP_400_BAD_REQUEST)

class GoalListCreateAPIView(ListCreateAPIView):
    serializer_class = GoalSerializer

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        return serializer.save(created_by=User.objects.get(id=user_id))

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
        user_id = self.kwargs.get('user_id')
        return serializer.save(created_by=User.objects.get(id=user_id), goal=Goal.objects.get(id=goal_id))
    
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
    
class DiaryFeedListAPIView(ListAPIView):
    serializer_class = DiarySerializer
    pagination_class = CustomCursorPagination
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        queryset = Diary.objects.filter((Q(created_by__in=user.following.all()) & Q(visibility='FL')) | Q(visibility='PB'))
        return queryset
    

    

