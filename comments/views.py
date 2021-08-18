from posts.models import Posts
from users.models import Register
from .models import Comments
from rest_framework.views import APIView,status
from rest_framework.response import Response
from .serializers import commentSerializers


class commentByUser(APIView):
    def get(self,request,format=None):
        # user=request.data['user'] 
        user='kedernath.mallick.tint023@gmail.com'
        if Register.objects.filter(email=user).exists():
            comments=Comments.objects.filter(owner__email=user).values()
            serialized_data=commentSerializers(comments,many=True)
            return Response(serialized_data.data,status.HTTP_200_OK)
        else:
            return Response("user does not exists",status.HTTP_204_NO_CONTENT)

class commentViewByPostId(APIView):
    def get(self,request,pk,format=None):
        post_id=pk
        if Posts.objects.filter(id__iexact=post_id).exists():
            comments=Comments.objects.filter(post__id=post_id).values()
            serialized_data=commentSerializers(comments,many=True)
            return Response(serialized_data.data,status.HTTP_200_OK)
        else:
            return Response("No comments.",status.HTTP_204_NO_CONTENT)

class CommentsById(APIView):
    def get(self,request,pk,format=None):
        comment_id=pk
        if Comments.objects.filter(comment_id=comment_id).exists():
            comments=Comments.objects.filter(comment_id=comment_id).values()
            serialized_data=commentSerializers(comments,many=True)
            return Response(serialized_data.data,status.HTTP_200_OK)
        else:
            return Response("No comments.",status.HTTP_204_NO_CONTENT)
    def put(self,request,pk,format=None):
        comment_id=pk
        if Comments.objects.filter(comment_id=comment_id).exists():
            comment_instance=Comments.objects.get(comment_id=comment_id)
            comment_serializer=commentSerializers(instance=comment_instance,data=request.data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response("successfully updated",status.HTTP_200_OK)
            else:
                return Response(comment_serializer.error_messages,status.HTTP_400_BAD_REQUEST)
        else:
            return Response("comment doest not exist",status.HTTP_204_NO_CONTENT)
    def delete(self,request,pk,format=None):
        comment_id=pk
        if Comments.objects.filter(comment_id=comment_id).exists():
            Comments.objects.filter(comment_id=comment_id).delete()
            return Response("comments successfully deleted",status.HTTP_200_OK)
        else:
            return Response("comment does not exist",status.HTTP_204_NO_CONTENT)

class createComment(APIView):
    def get(self,request,format=None):
        comments=Comments.objects.all()
        serialized_data=commentSerializers(comments,many=True)
        return Response(serialized_data.data,status.HTTP_200_OK)
    def post(self,request,format=None):
        request=request.data
        user=request['user']
        p=request['post']
        post_id=p['post_id']
        if Posts.objects.filter(id__iexact=post_id).exists():
            owner=Register(
                        email=user['email']
                    )
            post=Posts(
                        id=p['post_id'])
            post.owner=owner
            comments=Comments(
                    comment=request['comment'])
            comments.owner=owner
            comments.post=post
            comments.save()
            return Response("Comments created successfully.",status.HTTP_201_CREATED)
        else:
            return Response("Post doest not available.",status.HTTP_204_NO_CONTENT)