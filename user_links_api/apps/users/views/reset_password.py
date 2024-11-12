from django.contrib.auth.hashers import make_password

from ..models import User
from ..serializers import UserUpdateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class ResetPasswordView(APIView):

    def post(self,request,user_id):    
        try:
            password = make_password(request.POST['password'])
            data = {'password':password}
            instance = User.objects.get(pk=user_id)
            serializer = UserUpdateSerializer (data=data,instance=instance)
            serializer.is_valid(raise_exception=True)
            
        except Exception as exs:
            return Response({'Error':exs})
    
        else:
            serializer.save()
            return Response ({'Password':'Reseted'})