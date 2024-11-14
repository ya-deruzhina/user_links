from rest_framework import serializers
from ..models import LinksModel

class LinksUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    kind_link= serializers.ChoiceField (choices= LinksModel.KIND_LINKS,required=False)

    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance