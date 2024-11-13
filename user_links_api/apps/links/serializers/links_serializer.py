from rest_framework import serializers
from ..models import LinksModel
        
class LinksSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinksModel
        fields ='__all__'
                
        def create(self, validated_data):
            return LinksModel.objects.get_or_create(**validated_data)