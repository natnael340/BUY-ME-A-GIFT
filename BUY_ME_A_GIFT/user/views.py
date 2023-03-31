from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserLoginSerializers, UserRegisterSerializers, PasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.views import PasswordResetView
# Create your views here.
class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializers
    def post(self, request):
        seralizer = self.serializer_class(data=request.data)
        seralizer.is_valid(raise_exception=True)
        user = seralizer.validated_data['user']
        token = RefreshToken.for_user(user)

        return Response({'token': str(token.access_token), 'refresh': str(token)})

class SignUpView(GenericAPIView):
    serializer_class = UserRegisterSerializers
    def post(self, request):
        seralizer = self.serializer_class(data=request.data)
        seralizer.is_valid(raise_exception=True)
        user = seralizer.save()
        token = RefreshToken.for_user(user)
        

        return Response({'token': str(token.access_token), 'refresh': str(token)})

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    
    def post(self, request):
        serilaizer = self.serializer_class(data=request.data)
        if serilaizer.is_valid(raise_exception=True):
            email = serilaizer.validated_data['email']


def sendRestPasswordMessage(request, email):
    PasswordResetView.as_view()(request=request, email_template_name='')