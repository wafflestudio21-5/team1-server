from django.urls import path
from . import views

urlpatterns = [

    # goal, todo API views
    path('<int:user_id>/goals', views.GoalListCreateAPIView.as_view()),
    path('<int:user_id>/goals/<int:goal_id>', views.GoalDetailAPIView.as_view()), 
    path('<int:user_id>/goals/<int:goal_id>/todos', views.TodoListCreateAPIView.as_view()),
    path('<int:user_id>/goals/<int:goal_id>/todos/<int:todo_id>', views.TodoDetailAPIView.as_view()),
    
    # diary API views
    path('<int:user_id>/diary-create', views.DiaryCreateAPIView.as_view()),
    path('<int:user_id>/diaries', views.DiaryListAPIView.as_view()),
    path('<int:user_id>/diaries/<int:diary_id>', views.DiaryDetailAPIView.as_view()),
]