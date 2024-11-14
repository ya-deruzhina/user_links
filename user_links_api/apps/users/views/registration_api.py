from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from ..serializers import UserSerializer
from ..models import User


class UserRegistrationView(APIView):
    def post(self,request):
        try:
            data = request.data
            user = User.objects.filter(email=data['email'])
            if len(user)>0:
                status = HTTP_403_FORBIDDEN
                return Response({'Status':'Unsuccessful: This email is registered'},status=status)
            data['password'] = make_password(data['password'])
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except:
            status = HTTP_400_BAD_REQUEST
            return Response({'Status':'Unsuccessful: Invalid Data'},status=status)

        else:
            serializer.save()
            return Response({'Status':'Successful'})