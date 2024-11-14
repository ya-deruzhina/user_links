from ..models import User
from ..serializers import UserSerializer, UserUpdateSerializer

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,HTTP_403_FORBIDDEN
from django.contrib.auth.hashers import make_password


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(instance=user)
        
        except:
            status = HTTP_401_UNAUTHORIZED
            return Response({'Status':'User UNAUTHORIZED'},status=status)
        
        else:   
            data = serializer.data['email']  
            return Response ({'email':data})
        
    def patch (self,request):    
        try:
            user_id = request.user.id
            data=request.POST
            instance = User.objects.get(pk=user_id)

        except:
            status = HTTP_401_UNAUTHORIZED
            return Response({'Status':'Not Updated: User UNAUTHORIZED'},status=status)
            
        else:
            data = dict(filter(lambda x: x[1] !='', data.items()))
            keys_by_update = list(data.keys())

            if "password" in keys_by_update:
                data['password'] = make_password(data['password'])
            
            if "email" in keys_by_update:
                user = User.objects.filter(email=data['email'])
                if len(user)>0:
                    status = HTTP_403_FORBIDDEN
                    return Response({'Status':'Unsuccessful: This email is registered'},status=status)

            try:
                serializer = UserUpdateSerializer (data=data,instance=instance)
                serializer.is_valid(raise_exception=True)
            
            except:
                status = HTTP_400_BAD_REQUEST
                return Response({'Status':'Not Updated: Invalid Data'},status=status)
    
            else:
                serializer.save()
                return Response({'Status':f'Updated: {keys_by_update}'})
        
