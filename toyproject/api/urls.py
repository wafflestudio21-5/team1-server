from django.urls import path
from . import views

urlpatterns = [

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
    path('<int:user_id>/diarys/<int:diary_id>', views.DiaryDetailAPIView.as_view()),
]