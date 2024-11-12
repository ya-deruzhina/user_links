from apps.collections.models import CollectionModel
from apps.collections.serializers import CollectionSerializer,CollectionUpdateSerializer

from core import IsActive
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class CollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self,request,collection_id):
        try:
            collection = CollectionModel.objects.get(id=collection_id)
            serializer = CollectionSerializer(instance=collection)

        except:
            return Response({'Error':"not found"})
        
        else:
            return Response ({"results":serializer.data})
        
        
    def patch (self,request,collection_id):
        try:
            data = request.POST
            instance = CollectionModel.objects.get(pk = collection_id)
            serializer = CollectionUpdateSerializer (data=data,instance=instance)
            serializer.is_valid(raise_exception=True)
        
        except Exception as exs:
            return Response({'Error':exs})
        
        else:
            serializer.save()
            collection = CollectionModel.objects.get(id=collection_id)
            serializer = CollectionSerializer(instance=collection)
            return Response ({"results":serializer.data})
        
    def delete(self,request,collection_id):
        try:
            collection = CollectionModel.objects.get(id=collection_id)
    
        except Exception as exs:
            return Response({'Error':exs})
        
        else:
            collection.delete()
            return Response({'Status':"Deleted"})