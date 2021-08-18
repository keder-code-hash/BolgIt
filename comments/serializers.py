from users.models import Register
from posts.models import Posts
from django.db.models import fields
from rest_framework import serializers
from .models import Comments

class commentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=['comment_id','comment','post_id','owner_id','created']
    
    def update(self, instance, validated_data):
        instance.comment=validated_data.get('comment',instance.comment)
        instance.save()
        return instance