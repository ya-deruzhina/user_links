from apps.links.models import LinksModel
from apps.links.serializers import LinksSerializer


class LinkService:
    model = LinksModel

    @classmethod
    def create(cls, data):
        serializer = LinksSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data

