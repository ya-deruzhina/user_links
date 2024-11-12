from rest_framework import serializers
from apps.collections.models import CollectionModel
        
class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionModel
        fields ='__all__'
                
        def create(self, validated_data):
            return CollectionModel.objects.get_or_create(**validated_data) 

        def update(self,instance,validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance