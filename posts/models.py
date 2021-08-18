from django.db import models
from users.models import Register
from django_editorjs_fields import EditorJsJSONField,EditorJsTextField

class Posts(models.Model):
    post_title=models.CharField(blank=False,max_length=100)
    catagory=models.CharField(blank=False,max_length=30)
    body_custom = EditorJsTextField(
        plugins=[
            '@editorjs/paragraph',
            '@editorjs/image',
            '@editorjs/header',
            '@editorjs/list',
            '@editorjs/checklist',
            '@editorjs/quote',
            '@editorjs/raw',
            '@editorjs/code',
            '@editorjs/inline-code',
            '@editorjs/embed',
            '@editorjs/delimiter',
            '@editorjs/warning',
            '@editorjs/link',
            '@editorjs/marker',
            '@editorjs/table',
            "editorjs-github-gist-plugin",
            "editorjs-hyperlink",
        ],
        tools={
            "Gist": {
                "class": "Gist"
            },
            "LinkTool":{
              "class":"LinkTool",
              "inlineToolbar": True,
              "config":{
                  'endpoint': 'http://localhost:8000/fetchUrl/',
              }
            },
            "Image": {
                "config": {
                    "endpoints": {
                        "byFile": '/uploadImage/',
                        "byUrl": '/uploadImage/',
                        "additionalRequestHeaders":[{'Content-Type':'multipart/form-data'}],
                        'EDITORJS_IMAGE_NAME_ORIGINAL':True,
                    },
                }
            }
        },
        null=True,
        blank=True,
    )
    owner=models.ForeignKey(Register,on_delete=models.CASCADE)
    status=models.CharField(default='',blank=False,max_length=5)
    post_created=models.DateTimeField(auto_now_add=True)
    # modified_at=models.DateTimeField(auto_now_add=True,default=timezone.now)
    # post_like=models.IntegerField(default=0)
    def __str__(self):
        return self.post_title
    class Meta:
        ordering=['post_title']


# class PostLike(models.Model):
#    post_id=models.ForeignKey(Posts,on_delete=models.CASCADE)
#    user_id=models.ForeignKey(Register,on_delete=models.CASCADE)
#    isLiked=models.BooleanField(default=False)
#    def __str__(self):
#        return self.post_id_id

# class PostSave(models.Model):
#     post_id=models.ForeignKey(Posts,on_delete=models.CASCADE)
#     user_id=models.ForeignKey(Register,on_delete=models.CASCADE)
#     isSaved=models.BooleanField(default=False)
#     def __str__(self):
#         return self.post_id_id
    
