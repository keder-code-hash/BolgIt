from typing import OrderedDict
from django.db.models.fields import EmailField
from django.http.request import QueryDict
from django_editorjs_fields import fields
from rest_framework.exceptions import ValidationError
from .models import Posts, postTag,Comments
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

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect 
from .forms import NewCommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    posts=get_object_or_404(Posts,id=pk)
    values=list(Posts.objects.filter(id=pk).values('body_custom'))
    rate=PostRate.objects.filter(user_id__email=email_id).filter(post_id__id=pk)
    postOwner=posts.owner
    # print(postOwner)
    otherPosts=Posts.objects.filter(owner=postOwner).filter(status='p').order_by('post_created')
    # print(otherPosts)
    allDict=list(rate.values())
    avg=0
    if len(allDict)!=0:
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

    # post = get_object_or_404(Posts,id=pk)
    # Comments.objects.filter(id__lt=25).delete()
    allcomments = Comments.objects.filter(status=True).filter(post__id=pk)
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = posts
            user_comment.owner = Register.objects.get(email=email_id)
            user_comment.save()
            return HttpResponseRedirect('/post/'+str(pk))
        else:
            comment_form = NewCommentForm()
    comment_form = NewCommentForm()
    context={
            'other_post':otherPosts,
            'posts':posts,
            'body_custom':json_values,
            'is_authenticated':is_authenticated,
            'postRate':int(avg),
            'comment_form': comment_form,
            'allcomments': allcomments ,
            'user_name':email_id,
            # 'avtar_url':
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
        # print(catagory)
        status=request.POST.get('postStatus')
        data=request.POST.get('postData')
        # print(len(title))
        if status is None:
            status="d"
        ret_stat=False
        if title is not None and title is not None:
            try:
                post=Posts(post_title=title,catagory=catagory,body_custom=data,status=status,owner=user)
                post.save()
                for tag in catagory.split(","):
                    try:
                        t=postTag.objects.get(tag_name=tag)
                        post.tag.add(t)
                    except postTag.DoesNotExist:
                        t=postTag(tag_name=tag)
                        t.save()
                        post.tag.add(t)
                ret_stat=True
            except Posts.DoesNotExist:
                ret_stat=False
        else:
            ret_stat=False
        return JsonResponse(ret_stat,safe=False)
    Tags=postTag.objects.all().values()
    allTags=[]
    # print(Tags)
    for i in Tags:
        allTags.append(i.get('tag_name'))
    context={
        'is_authenticated': is_authenticated_user(request),
        'tags':allTags
    }
    return render(request,'createPost.html',context)

def UserPostView(request):
    access = request.COOKIES.get('accesstoken')
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get('email')
    user = Register.objects.get(email__iexact=email_id)
    if request.method=="GET":
        if user is not None:
            PostData=Posts.objects.filter(owner__email__iexact=email_id).values()
            for pData in PostData:
                relatedTags=postTag.objects.filter(posts__id=pData.get('id')).values()
                pData['tags']=relatedTags
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

                relatedTags=postTag.objects.filter(posts__id=pk).values()
                relatedTagList=[]
                for t in relatedTags:
                    relatedTagList.append(t.get('tag_name'))
                prevTagSet=set(relatedTagList)
                newTagSet=set(values['catagory'].split(","))
                deleteTags=prevTagSet.difference(newTagSet)
                for delTags in list(deleteTags):
                    obj.tag.filter(tag_name=delTags).delete()
                print(values['catagory'].split(","))
                for newTags in values['catagory'].split(","):
                    try:
                        t=postTag.objects.get(tag_name=newTags)
                        obj.tag.add(t)
                    except postTag.DoesNotExist:
                        newTag=postTag(tag_name=newTags)
                        newTag.save()
                        print(newTag)
                        obj.tag.add(newTag)

            except Posts.DoesNotExist:
                obj=Posts(**values)
                obj.save()
            # print(values)
            return JsonResponse(True,safe=False)

        postData=Posts.objects.get(id=pk)
        values=list(Posts.objects.filter(id=pk).values('body_custom'))
        json_values=json.dumps(values[0])
        Tags=postTag.objects.all().values()
        initTags=postTag.objects.filter(posts__id=pk).values()
        initialTags=[]
        allTags=[]
        # print(Tags)
        for it in initTags:
            initialTags.append(it.get('tag_name'))
        for i in Tags:
            allTags.append(i.get('tag_name'))
        context = {
                'id':pk,
                'body_custom':json_values,
                'data':postData,
                'is_authenticated': auth,
                'tags':allTags,
                'initTags':initialTags
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



def post_single(request):

    post = get_object_or_404(Posts,id=9)


    # Comments.objects.filter(id__lt=25).delete()
    allcomments = Comments.objects.filter(status=True).filter(post__id=9)
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.owner = Register.objects.get(email='keder123@gmail.com')
            user_comment.save()
            return HttpResponseRedirect('/comment/')
        else:
            comment_form = NewCommentForm()
    comment_form = NewCommentForm()

    return render(request, 'comments.html', {'comment_form': comment_form, 'allcomments': allcomments })


def addcomment(request):

    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            print(id)
            c = Comments.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = NewCommentForm(request.POST)
            # print(comment_form)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                result = comment_form.cleaned_data.get('comment')
                user = 'keder123@gmail.com'
                user_comment.owner = Register.objects.get(email='keder123@gmail.com')
                user_comment.post=Posts.objects.get(id=9)
                user_comment.save()
                comment_id=Comments.objects.filter(comment=result).order_by('-created').values_list()
                # print(list(comment_id[0])[0])
                return JsonResponse({'result': result, 'user': user,'comment_id': list(comment_id[0])[0]})








