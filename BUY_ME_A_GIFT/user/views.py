from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserLoginSerializers, UserRegisterSerializers, PasswordResetSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
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
        return {'request': self.request}
    def post(self, request):
        serilaizer = self.serializer_class(data=request.data, context={'request': request})
        serilaizer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset link was successfully sent to your email'})
            
class PasswordResetTokenCheckView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False,'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, "message": 'valid token'}, status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError as e:
            return Response({'success': False,'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordApiView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password succesfully changed'})
