from rest_framework.response import Response

from ..models import User
from ..serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(instance=user)
        
        except Exception as exs:
            return Response({'Error':exs})
        
        else:     
            return Response ({"results":serializer.data})
        
