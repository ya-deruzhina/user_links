from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import UserSerializer
from ..models import User


class UserRegistrationView(APIView):
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

        except Exception as exs:
            return Response({'Error':exs})

        else:
            serializer.save()
            user = User.objects.get (username = request.POST.get('username'))
            pas = request.POST.get('password')
            passw = make_password(pas)
            user.password = passw
            user.save() 
            return Response(serializer.data)