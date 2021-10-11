from django.db import models
from users.models import Register
from django_editorjs_fields import EditorJsJSONField,EditorJsTextField

class Posts(models.Model):
    post_title=models.CharField(blank=False,max_length=100)
    catagory=models.CharField(blank=False,max_length=30)
    body_custom =models.JSONField(null=True)
    owner=models.ForeignKey(Register,on_delete=models.CASCADE)
    status=models.CharField(default='',blank=False,max_length=5)
    post_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post_title
    class Meta:
        ordering=['post_title']


class PostRate(models.Model):
   post_id=models.ForeignKey(Posts,on_delete=models.CASCADE)
   user_id=models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
   rating=models.IntegerField(default=0,null=True)
   def __str__(self):
       return self.post_id_id

# class PostSave(models.Model):
#     post_id=models.ForeignKey(Posts,on_delete=models.CASCADE)
#     user_id=models.ForeignKey(Register,on_delete=models.CASCADE)
#     isSaved=models.BooleanField(default=False)
#     def __str__(self):
#         return self.post_id_id
    
class postTag(models.Model):
    tag_name=models.CharField(max_length=50,blank=False,default="NULL")
    def __str__(self) -> str:
        return self.tag_name