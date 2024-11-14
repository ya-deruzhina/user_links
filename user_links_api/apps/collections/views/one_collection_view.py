from ..models import CollectionModel
from ..serializers import CollectionSerializer,CollectionUpdateSerializer

from apps.links.models import LinksModel
from apps.links.serializers import LinksSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND


class CollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self,request,collection_id):
        try:
            collection = CollectionModel.objects.get(id=collection_id, owner = request.user.id)
            serializer = CollectionSerializer(instance=collection)

            links_inside = LinksModel.objects.filter(collection__id=collection_id)
            links = []
            for link in links_inside:
                links_data = LinksSerializer(instance=link).data
                links.append(links_data)

        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':"Sent Invalid Data"},status=status)
        
        else:
            result = serializer.data
            result['links'] = links
            return Response (result)
        
        
    def patch (self,request,collection_id):
        try:
            data = request.POST
            instance = CollectionModel.objects.get(pk = collection_id, owner = request.user.id)
            serializer = CollectionUpdateSerializer (data=data,instance=instance)
            serializer.is_valid(raise_exception=True)
        
        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':"Sent Invalid Data"},status=status)
        
        else:
            serializer.save()
            collection = CollectionModel.objects.get(id=collection_id)
            serializer = CollectionSerializer(instance=collection)
            return Response (serializer.data)
        
    def delete(self,request,collection_id):
        try:
            collection = CollectionModel.objects.get(id=collection_id, owner = request.user.id)
    
        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':'Sent Invalid Data'},status=status)
        
        else:
            collection.delete()
            return Response({'Status':"Deleted"})