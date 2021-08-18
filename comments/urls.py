from django.urls import path
from . import views
urlpatterns=[
    path('createcomment',views.createComment.as_view()),
    path('commentByuser',views.commentByUser.as_view()),
    path('commentbypost/<int:pk>/',views.commentViewByPostId.as_view()),
    path('comment/<int:pk>/',views.CommentsById.as_view())
]