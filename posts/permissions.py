from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import permissions
from .models import Posts

class IsOwnerOfPost(permissions.BasePermission):
    message = 'Please Log in yourself.'
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                url=request.path_info
                fun,args,kwargs=resolve(urlparse(url)[2])
                id=kwargs['pk']
                owner=Posts.objects.filter(id=id).values('owner')[0].get('owner')
                return request.user.email==owner and request.user.is_authenticated
        else:
            return False
