from users.models import Register
from rest_framework import serializers
from .models import Posts
from users.serializers import userSerializer

class post_view(serializers.ModelSerializer):
    owner=Register()
    class Meta:
        model=Posts
        fields=['id','post_title','content','catagory','owner','post_created']
        
class post_update_serializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        fields=['post_title','content','catagory','owner']
        read_only_fields = ['owner']

    def update(self,instance,validated_data):
        instance.post_title=validated_data.get('post_title',instance.post_title)
        instance.content=validated_data.get('content',instance.content)
        instance.catagory=validated_data.get('catagory',instance.catagory)
        instance.save()
        return instance