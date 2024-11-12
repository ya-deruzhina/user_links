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
            serializer = UserSerializer(data=user)
            import pdb; pdb.set_trace()
            serializer.is_valid(raise_exception=True)
        
        except Exception as exs:
            return Response({'Error':exs})
        
        else:     
            return (serializer.data)