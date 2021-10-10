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
from .models import PostRate



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
    if access is not None:
        decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
        email_id = decoded_data.get('email')
    else: 
        email_id=None
    posts=Posts.objects.get(id=pk)
    values=list(Posts.objects.filter(id=pk).values('body_custom'))
    rate=PostRate.objects.filter(user_id__email=email_id).filter(post_id__id=pk)
    postOwner=posts.owner
    # print(postOwner)
    otherPosts=Posts.objects.filter(owner=postOwner).filter(status='p').order_by('post_created')
    # print(otherPosts)
    allDict=list(rate.values())
    avg=allDict[0].get('rating')
    if email_id is None:
        avg=0
        noOfQuery=len(allDict)
        avg=0
        for i in allDict:
            avg+=i.get('rating')
        avg/=noOfQuery
    # print(list(rate.values()))
    print(avg)
    json_values=json.dumps(values[0])
    context={
            'other_post':otherPosts,
            'posts':posts,
            'body_custom':json_values,
            'is_authenticated':is_authenticated,
            'postRate':int(avg)
        }
    return render(request,'postView.html',context)

@csrf_exempt
def createPostView(request):
    access = request.COOKIES.get('accesstoken')
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get('email')
    user = Register.objects.get(email__iexact=email_id)
    if request.method=="POST":
        title=request.POST.get('postTitle')
        catagory=request.POST.get('postCatagory')
        status=request.POST.get('postStatus')
        data=request.POST.get('postData')
        print(len(title))
        if status is None:
            status="d"
        ret_stat=False
        if len(title)>0 and len(catagory)>0:
            try:
                Posts.objects.create(post_title=title,catagory=catagory,body_custom=data,status=status,owner=user)
                ret_stat=True
            except Posts.DoesNotExist:
                ret_stat=False
        else:
            ret_stat=False
        return JsonResponse(ret_stat,safe=False)
    context={
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

@csrf_exempt
def UpdatePost(request,pk):
    try:
        auth=is_authenticated_user(request)
        if request.method=="POST":
            values={
                'post_title':request.POST.get('postTitle'),
                'catagory':request.POST.get('postCatagory'),
                'body_custom':request.POST.get('postData'),
                'status':request.POST.get('postStatus')
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
            return JsonResponse(True,safe=False)
        postData=Posts.objects.get(id=pk)
        values=list(Posts.objects.filter(id=pk).values('body_custom'))
        json_values=json.dumps(values[0])
        context = {
                'id':pk,
                'body_custom':json_values,
                'data':postData,
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

@csrf_exempt
def rate(request):
    if request.method=="POST":
        ratingValue=request.POST.get("postTitle")
        postId=request.POST.get("postId")
        print(ratingValue,postId)
        if request.COOKIES.get('accesstoken') is not None:
            access = request.COOKIES.get('accesstoken')
            decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
            email_id = decoded_data.get('email')
            user = Register.objects.get(email__iexact=email_id)
            rateValues={
                'post_id':Posts.objects.get(id=postId),
                'user_id':user,
                'rating':ratingValue
            }
            try:
                obj=PostRate.objects.get(post_id=postId,user_id=email_id)
                for key,value in rateValues.items():
                    setattr(obj,key,value)
                obj.save()
            except PostRate.DoesNotExist:
                obj=PostRate(**rateValues)
                obj.save()
        else:
            PostRate.objects.create(post_id=Posts.objects.get(id=postId),rating=ratingValue)
        return JsonResponse(True,safe=False)