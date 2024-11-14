from ..serializers import CollectionSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

class CollectionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            data = request.POST
            user_id = request.user.id
            data = {
                'owner': user_id,
                'name':data['name'],
                'description':data['description']
            }
            serializer = CollectionSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except:
            status = HTTP_400_BAD_REQUEST
            return Response({'Status':'Sent Invalid Data'},status=status)
        
        else:
            serializer.save()
            return Response (serializer.data)