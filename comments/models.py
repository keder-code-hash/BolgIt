from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from posts.models import Posts
from users.models import Register

class Comments(models.Model):
    comment_id=models.BigAutoField(primary_key=True,unique=True)
    comment=models.TextField(blank=False)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    owner=models.ForeignKey(Register,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment