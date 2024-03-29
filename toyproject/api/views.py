from rest_framework.generics import UpdateAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from .serializers import (  TodoSerializer,
                            TodoDetailSerializer,
                            ProfileTodoSerializer, 
                            GoalSerializer, 
                            DiarySerializer, 
                            FollowRelationSerializer, 
                            ProfileSerializer,
                            ProfileSearchAndAllSerializer,
                            SignUpSerializer,
                            PasswordChangeSerializer,
                            ChangeLoginProfileSerializer,
                            LikeSerializer,
                            CommentSerializer,
                            CommentEditSerializer,
                            ProfileTodoSearchSerializer,
                            EmailLoginSerializer,
                            KakaoLoginSerializer,
                            PasswordEmailSerializer,
                            TodoImageUploadSerializer,
                            TodoImageArchiveSerializer,
                            UserFollowUnfollowSerializer,
                            TodoTodaySerializer,
                        )
from .models import Goal, Todo, Diary, User, Profile, Comment, Like

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, PermissionDenied

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from django.http import Http404

from django.shortcuts import get_object_or_404

from django.db.models import Q, OuterRef, Subquery, Count

from datetime import datetime

from rest_framework.pagination import CursorPagination

from django.core.mail import EmailMessage

class UserAlreadyFollowedException(APIException):
    status_code = 400
    default_detail = "User has already been followed."

class UserAlreadyFollowedException(APIException):
    status_code = 400
    default_detail = "User is not following the other user."

class IsRefreshToken(BasePermission):
    def has_permission(self, request, view, obj):
        return 

class IsUserToken(BasePermission):
    def has_permission(self, request, view, obj):
        return request.user == obj.user

class CustomCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 3

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)
    
class TodoFeedCursorPagination(CursorPagination):
    ordering = '-user_id'
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)

class SearchCursorPagination(CursorPagination):
    ordering = '-user_id'
    page_size = 20

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)

class DiaryCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)

class UserAllCursorPagination(CursorPagination):
    ordering = '-user_id'
    page_size = 20

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)

class TodoImageArchiveCursorPagination(CursorPagination):
    ordering = '-date'
    page_size = 30

    def paginate_queryset(self, queryset, request, view=None):
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return super().paginate_queryset(queryset, request, view)

## Signup API Views

class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            # if null then return error
            if request.data['email'] == "":
                return Response({
                    "error_msg" : "Email cannot be empty"
                }, status=status.HTTP_200_OK)
            user = serializer.save()
            return Response({
                "result" : "SUCCESS",
                "email" : user.email,
                "user_id" : user.id,
                "token" : Token.objects.get(user=user).key
            }, status=status.HTTP_200_OK)
        return Response({
            "error_msg" : serializer.errors.get('email')[0]
        }, status=status.HTTP_400_BAD_REQUEST)


class SignUpKakaoAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            if request.data['kakao_id'] == '':
                return Response({
                    "error_msg" : "Kakao ID cannot be empty"
                }, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            return Response({
                "token" : Token.objects.get(user=user).key,
                "kakao_id" : user.kakao_id,
                "user_id" : user.id
            }, status=status.HTTP_200_OK)
        return Response({
            "error_msg" : serializer.errors.get('kakao_id')[0],
        }, status=status.HTTP_400_BAD_REQUEST)


class SignupGuestAPIView(RetrieveAPIView): 

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = User.objects.create()
        return Response({
            "token": Token.objects.get(user=user).key,
            "user_id": user.id
        }, status=status.HTTP_200_OK)


class LoginEmailAPIView(CreateAPIView):

    serializer_class = EmailLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try: 
            user = User.objects.get(email=request.data['email'])
            if user.password == request.data['password']:
                return Response({
                    "user_id" : user.id,
                    "token" : Token.objects.get(user=user).key
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error_msg" : "Wrong password",
                }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                    "result_code" : 1,
                    "result" : "FAIL",
                    "error_msg" : "User with this email does not exist",
                }, status=status.HTTP_200_OK)


class LoginKakaoAPIView(CreateAPIView):

    serializer_class = KakaoLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try: 
            user = User.objects.get(kakao_id=request.data['kakao_id'])
            return Response({
                "token" : Token.objects.get(user=user).key,
                "kakao_id" : user.kakao_id,
                "user_id" : user.id
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ChangePasswordAPIView(UpdateAPIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer
    lookup_url_kwarg = 'user_id'

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to change this user's password.")
        return User.objects.get(id=user_id)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if user.password == old_password:
            user.password = new_password
            user.save()
            return Response({
                "result" : "SUCCESS",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error_msg" : "Wrong password",
            }, status=status.HTTP_200_OK)

class UpdateLoginProfileAPIView(RetrieveUpdateAPIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = ChangeLoginProfileSerializer
    lookup_url_kwarg = 'user_id'

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to update this user's profile.")
        return User.objects.get(id=user_id)

    def put(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        if user.password == request.data['password']:
            if request.data['email'] != "":
                user.email = request.data['email']
            if request.data['kakao_id'] != "":
                user.kakao_id = request.data['kakao_id']
            user.save()
            return Response({
                "result" : "SUCCESS",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error_msg" : "Wrong password",
            }, status=status.HTTP_200_OK)

class DeleteUserAPIView(RetrieveUpdateAPIView):
    permissions_classes = [IsAuthenticated]
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to delete this user.")
        user.delete()
        return Response({
            "result" : "SUCCESS",
        }, status=status.HTTP_200_OK)


class GetPasswordEmailAPIView(CreateAPIView):
    serializer_class = PasswordEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try: 
            user = User.objects.get(email=request.data['email'])
            email = EmailMessage(
                'Your password',
                user.password,
                to=[user.email]
            )
            email.send()
            return Response({
                "result" : "SUCCESS",
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                "error_msg" : "User with this email does not exist",
            }, status=status.HTTP_200_OK)

        
# 1. create a separate ListAPIView for viewing other users' goals
# 2. change ListCreateAPIView's permission_class to custom 

class GoalListCreateAPIView(ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to create a goal for this user.")
        return serializer.save(created_by=User.objects.get(id=user_id))

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Goal.objects.filter(created_by=user)
    
    def get_serializer_context(self):
        date = self.request.query_params.get('date')
        return {'date': date}


class GoalDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'goal_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("Error: User not found")
        return Goal.objects.filter(created_by=user)

class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        goal_id = self.kwargs.get('goal_id')
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to create a todo for this user.")
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
    serializer_class = TodoDetailSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.auth.user)
    
class DiaryListAPIView(ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Diary.objects.filter(created_by=User.objects.get(id=user_id))
    
class DiaryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        obj = Diary.objects.get(created_by_id=self.kwargs['user_id'], date=date)
        return obj

    
class FollowRelationAPIView(RetrieveAPIView, UpdateAPIView):
    serializer_class = FollowRelationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.get(id=user_id)
    
    def get_queryset(self):
        request_user = self.get_object()
        return request_user.followers.all()

    def put(self, serializer, *args, **kwargs):
        user = self.get_object()
        user_followers = self.get_queryset()
        user_to_remove = self.request.data.get('user_to_remove')
        filtered_qs = user_followers.filter(id=user_to_remove)

        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to delete followers for this user.")

        if not filtered_qs.exists():
            raise UserAlreadyFollowedException(f'User {user_to_remove} is not in User {user}\'s followers list.')
        
        user.followers.remove(user_to_remove)

        return Response({'result': f'User {user_to_remove} has been removed from User {user}\'s followers list.'}, status=status.HTTP_200_OK)

class ProfileDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'user_id'
    
class DiaryFeedListAPIView(ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DiaryCursorPagination
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        request_user = self.request.auth.user
        if request_user != user:
            raise PermissionDenied("You do not have permission to view this user's diary feed.")
        queryset = Diary.objects.filter((Q(created_by__in=user.following.all()) & Q(visibility='FL')) | Q(visibility='PB'))
        return queryset.filter(Q(created_by__kakao_id__isnull=False) | Q(created_by__email__isnull=False))
    
class TodoFeedListAPIView(ListAPIView):
    serializer_class = ProfileTodoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoFeedCursorPagination
    
    def get_queryset(self):
        queryset = Profile.objects.filter(
            Q(user__todos__is_completed=True) &
            Q(user__todos__goal__visibility='PB')
        ).distinct()

        return queryset.filter(Q(user__kakao_id__isnull=False) | Q(user__email__isnull=False))

class TodoSearchAPIView(ListAPIView):
    serializer_class = ProfileTodoSearchSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoFeedCursorPagination
    
    def get_queryset(self):
        subquery = Todo.objects.filter(
            created_by=OuterRef('user'),
            goal__visibility='PB',
            title__icontains=self.request.query_params.get('title', '')
        ).values('created_by').order_by().annotate(count=Count('id')).values('count')[:1]

        queryset = Profile.objects.annotate(
            num_matching_todos=Subquery(subquery)
        ).filter(num_matching_todos__gt=0).distinct()

        return queryset.filter(Q(user__kakao_id__isnull=False) | Q(user__email__isnull=False))
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = self.request.query_params.get('title', '')
        return context

class DiaryLikeAPIView(CreateAPIView, UpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Like.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        diary_id = self.kwargs.get('diary_id')
        user_id = self.request.data.get('user')
        
        obj = queryset.filter(user=User.objects.get(id=user_id), content_type__model='diary', object_id=diary_id).first()
        return obj

    
    def perform_create(self, serializer):
        diary_id = self.kwargs.get('diary_id')
        user_id = self.request.data.get('user')
        diary = Diary.objects.get(id=diary_id)

        if Like.objects.filter(user=User.objects.get(id=user_id), content_type__model='diary', object_id=diary_id).exists():
            raise ValidationError(f'User {user_id} has already liked this diary.')

        return serializer.save(liked_object=diary)
    
    def perform_update(self, serializer):
        diary_id = self.kwargs.get('diary_id')
        emoji = self.request.data.get('emoji')
        diary = Diary.objects.get(id=diary_id)

        return serializer.save(liked_object=diary, emoji=emoji)
    
class TodoLikeAPIView(CreateAPIView, UpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Like.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        todo_id = self.kwargs.get('todo_id')
        user_id = self.request.data.get('user')
        
        obj = queryset.filter(user=User.objects.get(id=user_id), content_type__model='todo', object_id=todo_id).first()
        return obj
    
    def perform_create(self, serializer):
        todo_id = self.kwargs.get('todo_id')
        user_id = self.request.data.get('user')
        todo = Todo.objects.get(id=todo_id)

        if Like.objects.filter(user=User.objects.get(id=user_id), content_type__model='todo', object_id=todo_id).exists():
            raise ValidationError(f'User {user_id} has already liked this todo.')

        return serializer.save(liked_object=todo)
    
    def perform_update(self, serializer):
        todo_id = self.kwargs.get('todo_id')
        emoji = self.request.data.get('emoji')
        todo = Todo.objects.get(id=todo_id)

        return serializer.save(liked_object=todo, emoji=emoji)

class CommentLikeAPIView(CreateAPIView, UpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Like.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        comment_id = self.kwargs.get('comment_id')
        user_id = self.request.data.get('user')
        
        obj = queryset.filter(user=User.objects.get(id=user_id), content_type__model='comment', object_id=comment_id).first()
        return obj

    
    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        comment = Comment.objects.get(id=comment_id)

        return serializer.save(liked_object=comment)
    
    def perform_update(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        emoji = self.request.data.get('emoji')
        comment = Comment.objects.get(id=comment_id)

        return serializer.save(liked_object=comment, emoji=emoji)

class DiaryCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        diary_id = self.kwargs.get('diary_id')
        diary = Diary.objects.get(id=diary_id)
        return serializer.save(commented_object=diary)
    
class UserSearchAPIView(ListAPIView):
    serializer_class = ProfileSearchAndAllSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SearchCursorPagination

    def get_queryset(self):
        username = self.request.query_params.get('username')
        queryset = Profile.objects.filter(username__icontains=username)
        return queryset.filter(Q(user__kakao_id__isnull=False) | Q(user__email__isnull=False))
    
class UserAllAPIView(ListAPIView):
    serializer_class = ProfileSearchAndAllSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserAllCursorPagination
    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset.filter(Q(user__kakao_id__isnull=False) | Q(user__email__isnull=False))

class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        elif self.request.method in ['PATCH', 'PUT']:
            return CommentEditSerializer
        return CommentSerializer  # Default serializer
    
class TodoImageUploadAPIView(RetrieveUpdateAPIView):
    serializer_class = TodoImageUploadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
    lookup_url_kwarg = 'todo_id'

    def perform_update(self, serializer):
        image = self.request.data.get('image')
        serializer.save(image=image)

class TodoImageAllAPIView(ListAPIView):
    serializer_class = TodoImageArchiveSerializer
    pagination_class = TodoImageArchiveCursorPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.auth.user
        todos_with_images = Todo.objects.filter(created_by=user)
        return todos_with_images.exclude(image='')

class UserFollowAPIView(UpdateAPIView):
    serializer_class = UserFollowUnfollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        request_user_id = self.request.auth.user.id
        return User.objects.get(id=request_user_id)
    
    def get_queryset(self):
        request_user = self.get_object()
        return request_user.following.all()

    def put(self, serializer):
        request_user = self.get_object()
        request_user_following = self.get_queryset()
        user_to_follow = self.request.data.get('user_to_follow')
        filtered_qs = request_user_following.filter(id=user_to_follow)

        if filtered_qs.exists():
            raise UserAlreadyFollowedException(f'User {request_user} is already following {user_to_follow}.')
        request_user.following.add(user_to_follow)

        return Response({'result': f'User {request_user} is now following {user_to_follow}.'}, status=status.HTTP_200_OK)

class UserUnfollowAPIView(UpdateAPIView):
    serializer_class = UserFollowUnfollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        request_user_id = self.request.auth.user.id
        return User.objects.get(id=request_user_id)
    
    def get_queryset(self):
        request_user = self.get_object()
        return request_user.following.all()

    def put(self, serializer):
        request_user = self.get_object()
        request_user_following = self.get_queryset()
        user_to_unfollow = self.request.data.get('user_to_unfollow')
        filtered_qs = request_user_following.filter(id=user_to_unfollow)

        if not filtered_qs.exists():
            raise UserAlreadyFollowedException(f'User {request_user} is already not following User {user_to_unfollow}.')
        request_user.following.remove(user_to_unfollow)

        return Response({'result': f'User {request_user} has unfollowed {user_to_unfollow}.'}, status=status.HTTP_200_OK)
    
class TodoTodayAPIView(ListAPIView):
    serializer_class = TodoTodaySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        request_user = self.request.auth.user
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        today = datetime.now()
        if request_user == user:
            goals_with_todos_today = Goal.objects.filter(Q(created_by=user_id) & Q(todos__date=today.strftime('%Y-%m-%d'))).distinct()
        else:
            goals_with_todos_today = Goal.objects.filter((Q(created_by=user_id) & Q(todos__date=today.strftime('%Y-%m-%d'))) & (Q(visibility='PB') | (Q(visibility='FL') & Q(created_by__followers=request_user)))).distinct()
        return goals_with_todos_today
    