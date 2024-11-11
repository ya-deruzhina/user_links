from django.contrib.auth.hashers import make_password

from ..models import User
from ..serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.views import APIView
from rest_framework.response import Response

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# Transit Update
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    def post(self,request):    
        try:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            data=request.POST

        except Exception as exs:
            return Response({'Error':exs})
            
        else:
            inv_d = dict(filter(lambda x: x[1] !='', data.items()))
            keys_by_update = list(inv_d.keys())

            try:
                instance = User.objects.get(pk=user_id)
                serializer = UserSerializer (data=inv_d,instance=instance)
                serializer.is_valid(raise_exception=True)
            
            except Exception as exs:
                return Response({'Error':exs})
    
            else:
                serializer.save()
                return Response({'Status':'Updated'})