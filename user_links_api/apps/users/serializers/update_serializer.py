from rest_framework import serializers
from ..models import User



class UserUpdateSerializer(serializers.Serializer): 
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
   
    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance