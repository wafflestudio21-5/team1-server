from django.urls import path
from . import views

urlpatterns = [

    # login API views
    path('signup/email', views.SignUpAPIView.as_view()),
    path('signup/kakao', views.SignUpKakaoAPIView.as_view()),
    path('signup/guest', views.SignupGuestAPIView.as_view()),
    path('login/email', views.LoginEmailAPIView.as_view()),
    path('login/kakao', views.LoginKakaoAPIView.as_view()),

    # profile - update / delete
    path('<int:user_id>/update/password', views.ChangePasswordAPIView.as_view()),
    path('<int:user_id>/update/email', views.UpdateEmailAPIView.as_view()),
    path('<int:user_id>/update/kakao', views.UpdateKakaoAPIView.as_view()),
    path('<int:user_id>/update/delete', views.DeleteUserAPIView.as_view()),


    # profile / following_followers
    path('<int:user_id>', views.ProfileDetailAPIView.as_view()),
    path('<int:user_id>/follows', views.FollowRelationAPIView.as_view()),

    # goal, todo API views
    path('<int:user_id>/goals', views.GoalListCreateAPIView.as_view()),
    path('<int:user_id>/goals/<int:goal_id>', views.GoalDetailAPIView.as_view()), 
    path('<int:user_id>/goals/<int:goal_id>/todos', views.TodoListCreateAPIView.as_view()),
    path('<int:user_id>/goals/<int:goal_id>/todos/<int:todo_id>', views.TodoDetailAPIView.as_view()),
    
    # diary API views
    path('diary-create', views.DiaryCreateAPIView.as_view()),
    path('<int:user_id>/diarys', views.DiaryListAPIView.as_view()),
    path('<int:user_id>/diarys/<str:date>', views.DiaryDetailAPIView.as_view()),
    path('<int:user_id>/diaryfeed', views.DiaryFeedListAPIView.as_view()),
]