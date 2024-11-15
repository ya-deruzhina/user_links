from apps.collections.models import CollectionModel
from apps.collections.serializers import CollectionSerializer


class CollectionService:
    model = CollectionModel

    @classmethod
    def create(cls, data):
        serializer = CollectionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data


