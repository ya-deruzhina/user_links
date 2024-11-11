from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from core import NON_FIELD_ERRORS

from ..serializers import SignInSerializer
from ..services import AuthPayloadService, SignInService


class SignInView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            errors = serializer.errors

            if errors.get(NON_FIELD_ERRORS):
                status = HTTP_401_UNAUTHORIZED
            else:
                status = HTTP_400_BAD_REQUEST

            return Response({'errors': errors}, status=status)

        data = serializer.validated_data

        user = data['user']
        token = SignInService.login(request, user)

        response_data = AuthPayloadService.call(user, token)
        return Response(response_data)
