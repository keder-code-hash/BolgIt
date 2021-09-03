from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('postbytitle',views.PostViewByPostTitle.as_view()),
    path('postbyuser',views.PostViewByUser.as_view()),
    path('postbyid/<int:pk>/',views.PostViewById.as_view()),
    path('postcreate/',views.postView.as_view()),
    path('post/<int:pk>/',views.singlepostView,name='postView'),
    path('postCreate/',views.createPostView,name='createpost'),
    path('uploadImage/',views.upload_image_view,name='uploadimageview'),
    path('UserPostView/',views.UserPostView,name='allPostView'),
    path('updatePost/<int:pk>/',views.UpdatePost,name="postUpdate"),
    path('deletePost/',views.delPost,name="deletePost"),
    path('rate/',views.rate,name="rating")
    # path('likePost/',views.postLikeHandler,name='postLike'),
    # path('postsave/',views.savePostAjaxHandeler,name='savePost')
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)