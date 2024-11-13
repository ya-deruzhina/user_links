from ..models import LinksModel
from ..serializers import LinksSerializer

from core import IsActive

from rest_framework import generics
from rest_framework import pagination

class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class LinksView(generics.ListAPIView):
    permission_classes = (IsActive,)
    serializer_class = LinksSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return LinksModel.objects.filter(owner=self.request.user.id).order_by('-updated_at')