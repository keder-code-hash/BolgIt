from django.contrib import admin
from posts.models import Comments, Posts, postTag
# from django.contrib.admin


admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(postTag)
# Register your models here.
