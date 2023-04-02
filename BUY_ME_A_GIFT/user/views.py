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
    
    def get_serializer_context(self):
        return super().get_serializer_context()
    def post(self, request):
        serilaizer = self.serializer_class(data=request.data)
        serilaizer.is_valid(raise_exception=True)
            
class PasswordResetTokenCheckView(GenericAPIView):
    def get(self, request, uidb64, token):
        pass
