from ..models import CollectionModel
from ..serializers import CollectionSerializer

from rest_framework import generics
from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated

class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class CollectionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return CollectionModel.objects.filter(owner=self.request.user.id).order_by('name')