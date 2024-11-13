from ..models import LinksModel
from ..serializers import LinksSerializer,LinksUpdateSerializer

from core import IsActive
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class LinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self,request,link_id):
        try:
            link_data = LinksModel.objects.get(id=link_id)
            serializer = LinksSerializer(instance=link_data)

        except:
            return Response({'Error':"not found"})
        
        else:
            return Response ({"results":serializer.data})
        
        
    def patch (self,request,link_id):
        try:
            data = request.POST
            instance = LinksModel.objects.get(pk=link_id)
            serializer = LinksUpdateSerializer (data=data,instance=instance)
            serializer.is_valid(raise_exception=True)
        
        except:
            return Response({'Error':"not found"})
        
        else:
            serializer.save()
            collection = LinksModel.objects.get(id=link_id)
            serializer = LinksSerializer(instance=collection)
            return Response ({"results":serializer.data})
        
    def delete(self,request,link_id):
        try:
            collection = LinksModel.objects.get(id=link_id)
    
        except:
            return Response({'Error':"not found"})
        
        else:
            collection.delete()
            return Response({'Status':"Deleted"})