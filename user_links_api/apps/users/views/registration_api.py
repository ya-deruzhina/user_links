from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import UserSerializer
from ..models import User


class UserRegistrationView(APIView):
    def post(self,request):
        try:
            data = request.data
            data['password'] = make_password(data['password'])
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except Exception as exs:
            return Response({'Error':exs})

        else:
            serializer.save()
            data['username'] = serializer.data['username']
            data['first_name'] = serializer.data['first_name']
            data['email'] = serializer.data['email']
            return Response(data)