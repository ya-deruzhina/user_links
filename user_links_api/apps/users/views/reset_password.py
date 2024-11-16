from django.contrib.auth.hashers import make_password

from ..models import User
from ..serializers import UserUpdateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

class ResetPasswordView(APIView):

    def patch(self,request):    
        try:
            email = request.POST['email']
            password = make_password(request.POST['password'])
            data = {'password':password}
            instance = User.objects.get(email=email)
            serializer = UserUpdateSerializer (data=data,instance=instance)
            serializer.is_valid(raise_exception=True)
            
        except:
            status = HTTP_400_BAD_REQUEST
            return Response({'Status':'Unsuccessful: Invalid Data'},status=status)
    
        else:
            serializer.save()
            return Response ({'Status':'Successful'})