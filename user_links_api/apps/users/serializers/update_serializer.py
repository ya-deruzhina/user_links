from rest_framework import serializers
from ..models import User



class UserUpdateSerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=50,required=False)
    password = serializers.CharField(required=False)
    first_name = serializers.CharField(max_length=20,required=False)
    email = serializers.CharField(required=False)
   
    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance