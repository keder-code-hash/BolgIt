from users.jwtAuth import refresh_acsess_token
from django.contrib.auth.models import User
from django.urls import path
from django.urls.conf import include
from rest_framework.urlpatterns import format_suffix_patterns
import rest_framework
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Users,register_view,login_view,homeView,custom_log_out,userProfileView,upDateProfile
# from django.contrib.auth.views import logout


urlpatterns=[ 
    path('api/', Users.as_view()),
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('', homeView, name='homePage'),
    path('profile/',userProfileView,name='profile'),
    path('logout/',custom_log_out,name='logout'),
    path('updateProfile/', upDateProfile, name='updateProfile'),
    path('refreshtoken/',refresh_acsess_token),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)