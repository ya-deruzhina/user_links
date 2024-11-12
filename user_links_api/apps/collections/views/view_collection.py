from apps.collections.models import CollectionModel
from apps.collections.serializers import CollectionSerializer

from core import IsActive

from rest_framework import generics
from rest_framework import pagination

class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class CollectionsView(generics.ListAPIView):
    permission_classes = (IsActive,)
    serializer_class = CollectionSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return CollectionModel.objects.filter(owner=self.request.user.id).order_by('-name')