"""
This module contains views for User authentication and registration.

"""

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserLoginSerializers, UserRegisterSerializers, PasswordResetSerializer, SetNewPasswordSerializer, PasswordResetTokenCheckSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class LoginView(GenericAPIView):
    """
    Authenticate user with provided login credentials.

    Required fields in request data:
        - email
        - password
    Return access_token and refresh_token

    """
    serializer_class = UserLoginSerializers
    permission_classes=[AllowAny]

    @swagger_auto_schema(security=[])
    def post(self, request) -> Response:
        seralizer = self.serializer_class(data=request.data)
        seralizer.is_valid(raise_exception=True)
        user = seralizer.validated_data['user']
        token = RefreshToken.for_user(user)

        return Response({'token': str(token.access_token), 'refresh': str(token)})


class SignUpView(GenericAPIView):
    """
    Register a new user with provided details.

    Required fields in request data:
        - email
        - password

    Returns access and refresh token on successful registration.
    """
    serializer_class = UserRegisterSerializers
    permission_classes=[AllowAny]

    @swagger_auto_schema(security=[])
    def post(self, request: Request) -> Response:
        seralizer = self.serializer_class(data=request.data)
        seralizer.is_valid(raise_exception=True)
        user = seralizer.save()
        token = RefreshToken.for_user(user)
        

        return Response({'token': str(token.access_token), 'refresh': str(token)})

class PasswordResetView(GenericAPIView):
    """
    Send password reset link to user's email.

    Required fields in request data:
        - email

    Returns success message on successful email sending.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_serializer_context(self) -> dict:
        return {'request': self.request}

    @swagger_auto_schema(security=[])
    def post(self, request) -> Response:
        serilaizer = self.serializer_class(data=request.data, context={'request': request})
        serilaizer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset link was successfully sent to your email'})

class PasswordResetTokenCheckView(GenericAPIView):
    """
    Check validity of password reset token based on user id.

    Required path parameters:
        - uidb64: base64 encoded user id
        - token: password reset token

    Returns success message on valid token, error message on invalid or expired token.
    """
    serializer_class = PasswordResetTokenCheckSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(security=[])
    def get(self, request:Request, uidb64:str, token:str) -> Response:
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False,'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, "message": 'valid token'}, status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError as e:
            return Response({'success': False,'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(security=[])
class SetNewPasswordApiView(GenericAPIView):
    """
    Reset the password of a user.

    Required fields in request data:
        - uidb64: base64 encoded user id
        - token: password reset token
        - password: new password

    Changes the password of a user to the new password if the fields are valid.

    Returns success message on valid token, uuidb64, error message on invalid or expired token.
    """
    serializer_class = SetNewPasswordSerializer
    permission_classes=[AllowAny]

    @swagger_auto_schema(security=[])
    def patch(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password succesfully changed'})
