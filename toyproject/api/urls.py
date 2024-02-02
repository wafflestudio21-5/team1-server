from django.urls import path
from . import views

urlpatterns = [

    # login API views
    path('signup/email', views.SignUpAPIView.as_view()),
    path('signup/kakao', views.SignUpKakaoAPIView.as_view()),
    path('signup/guest', views.SignupGuestAPIView.as_view()),
    path('login/email', views.LoginEmailAPIView.as_view()),
    path('login/kakao', views.LoginKakaoAPIView.as_view()),

    # change profile api views
    path('<int:user_id>/update/password', views.ChangePasswordAPIView.as_view()),
    path('<int:user_id>/update/', views.UpdateLoginProfileAPIView.as_view()),
    path('<int:user_id>/delete', views.DeleteUserAPIView.as_view()),

    path('password-send-email', views.GetPasswordEmailAPIView.as_view()),

    # profile / following_followers
    path('<int:user_id>', views.ProfileDetailAPIView.as_view()),
    path('<int:user_id>/follows', views.FollowRelationAPIView.as_view()),

    # follow / unfollow API view
    path('follow', views.UserFollowAPIView.as_view()),
    path('unfollow', views.UserUnfollowAPIView.as_view()),

    # profile search API view
    path('user-search', views.UserSearchAPIView.as_view()),

    # todo search API view (not working yet)
    path('todo-search', views.TodoSearchAPIView.as_view()),

    # all user profiles
    path('user-all', views.UserAllAPIView.as_view()),

    # goal, todo API views
    path('<int:user_id>/goals', views.GoalListCreateAPIView.as_view()),
    path('<int:user_id>/goals/<int:goal_id>', views.GoalDetailAPIView.as_view()), 
    path('<int:user_id>/goals/<int:goal_id>/todos', views.TodoListCreateAPIView.as_view()),
    path('<int:user_id>/goals/<int:goal_id>/todos/<int:todo_id>', views.TodoDetailAPIView.as_view()),

    # todo shortcut: image upload API view
    path('image-upload/<int:todo_id>', views.TodoImageUploadAPIView.as_view()),
    
    # diary API views
    path('diary-create', views.DiaryCreateAPIView.as_view()),
    path('<int:user_id>/diarys', views.DiaryListAPIView.as_view()),
    path('<int:user_id>/diarys/<str:date>', views.DiaryDetailAPIView.as_view()),
    

    # feedlist API views
    path('<int:user_id>/diaryfeed', views.DiaryFeedListAPIView.as_view()),
    path('todofeed', views.TodoFeedListAPIView.as_view()),

    # like API views
    path('diarys/<int:diary_id>/like', views.DiaryLikeAPIView.as_view()),
    path('todos/<int:todo_id>/like', views.TodoLikeAPIView.as_view()),
    path('comments/<int:comment_id>/like', views.CommentLikeAPIView.as_view()),

    # comment API views
    path('diarys/<int:diary_id>/comment', views.DiaryCommentAPIView.as_view()),
    path('comment-detail/<int:comment_id>', views.CommentDetailAPIView.as_view()),

    # user todo images archive API views
    path('image-all', views.TodoImageAllAPIView.as_view()),

]