from ..models import LinksModel
from ..serializers import LinksSerializer,LinksUpdateSerializer

from apps.collections.models import CollectionModel

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND


class LinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self,request,link_id):
        try:
            link_data = LinksModel.objects.get(id=link_id,owner = request.user.id)
            serializer = LinksSerializer(instance=link_data)

        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':'Sent Invalid Data'},status=status)
        
        else:
            return Response (serializer.data)
        
        
    def patch (self,request,link_id):
        try:
            data = request.POST
            instance = LinksModel.objects.get(pk=link_id,owner = request.user.id)
            serializer = LinksUpdateSerializer (data=data,instance=instance)
            serializer.is_valid(raise_exception=True)

            if data['collection_add'] != '':
                collection = CollectionModel.objects.get(id=data['collection_add'])
                instance.collection.add(collection)

                instance.collection.get_or_create(id=data['collection_add'])
            if data['collection_remove'] != '':
                collection = CollectionModel.objects.get(id=data['collection_remove'])
                instance.collection.remove(collection)
        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':'Sent Invalid Data'},status=status)
        
        else:
            serializer.save()
            collection = LinksModel.objects.get(id=link_id)
            serializer = LinksSerializer(instance=collection)
            return Response (serializer.data)
        
    def delete(self,request,link_id):
        try:
            collection = LinksModel.objects.get(id=link_id,owner = request.user.id)
    
        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':'Sent Invalid Data'},status=status)
        
        else:
            collection.image.delete(save=True)
            collection.delete()
            return Response({'Status':"Deleted"})