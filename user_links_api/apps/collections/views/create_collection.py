from apps.collections.models import CollectionModel
from apps.collections.serializers import CollectionSerializer

from core import IsActive
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class CollectionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            data = request.POST
            serializer = CollectionSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except Exception as exs:
            return Response({'Error':exs})
        
        else:
            serializer.save()
            return Response (serializer.data)