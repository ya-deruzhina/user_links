from rest_framework import serializers
from ..models import CollectionModel 


class CollectionUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    short_description = serializers.CharField(required=False)

    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance