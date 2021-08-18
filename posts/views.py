from typing import OrderedDict
from django.db.models.fields import EmailField
from django.http.request import QueryDict
from django_editorjs_fields import fields
from rest_framework.exceptions import ValidationError
from .models import Posts
from users.models import Register
from .serializers import post_update_serializer
from .serializers import post_view
from rest_framework.views import APIView,status
from rest_framework.response import Response
from django.http import HttpResponse
from .permissions import IsOwnerOfPost
from django.shortcuts import redirect, render
from django.conf import settings
import jwt
from users.views import is_authenticated_user
from django.views.decorators.csrf import requires_csrf_token,ensure_csrf_cookie,csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from posts.forms import postsCreateForm
import json
from django.core.serializers.json import DjangoJSONEncoder

class PostViewByPostTitle(APIView):
    def get(self,request,foemat=None):
        # post_title=request.data['post_title']
        post_title='api_view@1'
        if Posts.objects.get(post_title__iexact=post_title):
            data=Posts.objects.filter(post_title__iexact=post_title)
            serialized_data=post_view(data,many=True)
            return Response(serialized_data.data,status.HTTP_200_OK)
        else:
            return Response("check the post title.",status.HTTP_204_NO_CONTENT)

class PostViewByUser(APIView):
    def get(self,request,format=None):
        # emailid=request.data['email']
        # emailid='kedernath.mallick.tint023@gmail.com'
        emailid=request.user.email
        if Posts.objects.filter(owner__email=emailid).exists():
            data=Posts.objects.filter(owner__email=emailid)
            serialized_data=post_view(data,many=True)
            return Response(serialized_data.data,status.HTTP_200_OK)
        else:
            return Response("user does not have any post",status.HTTP_204_NO_CONTENT)

class PostViewById(APIView):
    permission_classes=[IsOwnerOfPost]
    def get(self,request,pk,format=None):
        # id=request.data['id']
        post_id=pk
        if Posts.objects.filter(id__iexact=post_id).exists():
            data=Posts.objects.filter(id__iexact=post_id)
            serialized_data=post_view(data,many=True)
            return Response(serialized_data.data,status.HTTP_200_OK)
        else:
            return Response("post does not exist",status.HTTP_204_NO_CONTENT)
    def put(self,request,pk,format=None):
        post_id=pk
        if Posts.objects.filter(id__iexact=post_id).exists():
            post_instance=Posts.objects.get(id__iexact=post_id)
            post_updated_data=post_update_serializer(instance=post_instance,data=request.data)
            if post_updated_data.is_valid():
                post_updated_data.save()
                return Response("post successfully updated", status.HTTP_200_OK)
            else:
                return Response(post_updated_data.errors,status.HTTP_400_BAD_REQUEST)
        else:
            return Response("post doest not exist.Make a post first",status.HTTP_204_NO_CONTENT)
    def delete(self,request,pk,format=None):
        # post_id=request.data['id']
        post_id=pk
        if Posts.objects.filter(id__iexact=post_id).exists():
            Posts.objects.filter(id__iexact=post_id).delete()
            return Response("Post successfully deleted.",status.HTTP_200_OK)
        else:
            return Response("post does not exist")

class postView(APIView):
    def get(self,request,format=None):
        data=Posts.objects.all()
        serialized_data=post_view(data,many=True)
        return Response(serialized_data.data,status.HTTP_200_OK)
    def post(self,request,format=None):
        request=request.data
        user=request['user']
        if Register.objects.filter(email__iexact=user['email']).exists():
            owner=Register(
                email=user['email'])
            post=Posts(
                post_title=request['post_title'],
                content=request['content'],
                catagory=request['catagory'],
            )
            post.owner=owner
            post.save()
            return Response("Post succesfully created.",status.HTTP_200_OK)
        else:
            return Response("user doest not exist.Register yourself first",status.HTTP_204_NO_CONTENT)





# @requires_csrf_token
@csrf_exempt
def upload_image_view(request):
    file=request.FILES['image']
    fs=FileSystemStorage(location=settings.MEDIA_ROOT+'/uploads/Image')
    filename=file.name
    file=fs.save(filename,file)
    fileurl=settings.MEDIA_URL+'/uploads/Image/'+filename
    print(fileurl)
    return JsonResponse({
        'success':1,
        'file':{'url':fileurl}
    })


def singlepostView(request,pk):
    try:
        access = request.COOKIES.get('accesstoken')
        is_authenticated=False
        if access is not None:
            is_authenticated=True
    except ValueError as err:
        print(err)
    posts=Posts.objects.get(id=pk)
    values=list(Posts.objects.filter(id=pk).values('body_custom'))
    json_values=json.dumps(values[0])
    context={
            'posts':posts,
            'body_custom':json_values,
            'is_authenticated':is_authenticated,
        }
    return render(request,'postView.html',context)

def createPostView(request):
    access = request.COOKIES.get('accesstoken')
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get('email')
    user = Register.objects.get(email__iexact=email_id)
    if request.method=="POST":
        postStatus=OrderedDict(request.POST).get('status')
        form=postsCreateForm(request.POST)
        if form.is_valid():
            postData=form.save(commit=False)
            postData.owner=user
            postData.status=postStatus
            context = {
                'form': form,
                'is_authenticated': is_authenticated_user(request),
            }
            postData.save()
            return redirect('homePage')
    form=postsCreateForm()
    context={
        'form': form,
        'is_authenticated': is_authenticated_user(request),
    }
    return render(request,'createPost.html',context)

def UserPostView(request):
    access = request.COOKIES.get('accesstoken')
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get('email')
    user = Register.objects.get(email__iexact=email_id)
    if request.method=="GET":
        if user is not None:
            PostData=Posts.objects.filter(owner__email__iexact=email_id)
            context={
                'posts':PostData,
                'is_authenticated':True
            }
            print(context)
        else:
            print("user doesnot exist")
        return render(request,'UserPostView.html',context)

def UpdatePost(request,pk):
    try:
        auth=is_authenticated_user(request)
        if request.method=="POST":
            form=OrderedDict(request.POST)
            values={
                'post_title':form.get('post_title'),
                'post_catagory':form.get('post_catagory'),
                'body_custom':form.get('body_custom'),
                'status':form.get('status')
            }
            try:
                obj=Posts.objects.get(id=pk)
                for key,value in values.items():
                    setattr(obj,key,value)
                obj.save()
            except Posts.DoesNotExist:
                obj=Posts(**values)
                obj.save()
            # print(values)
            
        postData=Posts.objects.get(id=pk)
        form=postsCreateForm()
        context = {
                'id':pk,
                'form': form,
                'post':postData,
                'is_authenticated': auth,
            }
        return render(request,'postUpdate.html',context)
    except ValueError as err:
        print(err)

#check the db error
@csrf_exempt
def delPost(request):
    try:
        auth=is_authenticated_user(request)
        if request.method=='GET' and auth:
            id=request.GET.get('post_id')
            if id is not None:
                try:
                    Posts.objects.filter(id=id).delete()
                    return JsonResponse(True,safe=False)
                except Posts.DoesNotExist as ex:
                    return JsonResponse(False,safe=False)
            else:
                return JsonResponse(False,safe=False)
    except ValidationError as err:
        print(err)