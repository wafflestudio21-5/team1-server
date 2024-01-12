from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .serializers import SignUpSerializer, SignUpKakaoSerializer, EmailLoginSerializer, KakaoLoginSerializer
from .serializers import TodoSerializer, GoalSerializer, DiarySerializer, FollowRelationSerializer, TodoConciseSerializer, ProfileSerializer
from .models import Goal, Todo, Diary, User, Profile

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from django.http import Http404

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
                    "error_msg" : "User already exists",
                    "token" : "",
                    "user_id" : ""
                }, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                user = serializer.save(username=serializer.validated_data['email'])
                return Response({
                    "result_code" : 0,
                    "result" : "SUCCESS",
                    "error_msg" : "",
                    "token" : "10100010sdfasdfasemail",
                    "user_id" : user.id
                }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors,
            "token" : "",
            "user_id" : ""
        }, status=status.HTTP_400_BAD_REQUEST)


class SignUpKakaoAPIView(CreateAPIView):
    serializer_class = SignUpKakaoSerializer

    def post(self, request, *args, **kwargs):
        serializer = SignUpKakaoSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(username="kakao" + serializer.validated_data['kakao_id'])
            return Response({
                "result_code" : 0,
                "result" : "SUCCESS",
                "error_msg" : "",
                "token" : "10100010sdfasdfaskakao",
                "kakao_id" : user.kakao_id,
                "user_id" : user.id
            }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors,
            "token" : "",
            "kakao_id" : "",
            "user_id" : ""
        }, status=status.HTTP_400_BAD_REQUEST)



class SignUpGuestAPIView(CreateAPIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.create(username="guest" + str(User.objects.count()));
        return Response({
            "token": "10100010sdfasdfas",
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
                "token" : "10100010sdfasdfasemail"
            }, status=status.HTTP_200_OK)
        return Response({
            "result_code" : 1,
            "result" : "FAIL",
            "error_msg" : serializer.errors,
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
            user = serializer.validated_data
            return Response({
                "result_code" : 0,
                "result" : "SUCCESS",
                "error_msg" : "",
                "token" : "10100010sdfasdfaskakao"
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
        return serializer.save(created_by=self.request.user)
    
class DiaryListAPIView(ListAPIView):
    serializer_class = DiarySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Diary.objects.filter(created_by=User.objects.get(id=user_id))
    
class DiaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    lookup_url_kwarg = 'diary_id'
    
class FollowRelationAPIView(RetrieveAPIView):
    serializer_class = FollowRelationSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'

class ProfileDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'user_id'
    


