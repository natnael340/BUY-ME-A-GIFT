"""
This File contains serialization class for user related data.

It contains:
    Login infrmation serialization class
    Registration information serialization class
    Password resetting information serialization class

"""


from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.exceptions import AuthenticationFailed
class UserLoginSerializers(serializers.Serializer):
    """Serializer for User login."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs) -> dict:
        """Validate email and password for login."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('User is not active')
            else:
                raise serializers.ValidationError('Email or password is incorrect')
        else:
            raise serializers.ValidationError('Must include email and password')

class UserRegisterSerializers(serializers.Serializer):
    """Serializer for User registration."""
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')
        
    def create(self, validated_data) -> User:
        """Create a new User with Email and Password"""
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'])
        
        return user
        
class PasswordResetSerializer(serializers.Serializer): 
    """Serializer for password reset request."""    
    email = serializers.EmailField(required=True)    

    def validate(self, attrs) -> dict:
        """Validate the password reset request using the email"""
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
          
            current_site = get_current_site(self.context.get('request')).domain
            relativeUrl = reverse('password_reset', kwargs={'token': token, 'uidb64': uidb64})
            absoluteUrl = f'http://{current_site}/{relativeUrl}'.format(current_site, relativeUrl)
            email_body  = f"Hello, \n Here is your password reset url {absoluteUrl}".format(url=absoluteUrl)
            data = {"email_body": email_body, 'to_email': user.email, 'email_subject': 'Reset Password'}
                
            Util.send_email(data)
        else:
            raise serializers.ValidationError('User does not exist')
        
        return super().validate(attrs)
    
class PasswordResetTokenCheckSerializer(serializers.Serializer):
    """Serializer for checking the validity of password reset token."""
    pass
class SetNewPasswordSerializer(serializers.Serializer):
    """Serializer for setting new password given the token and uuid."""
    password = serializers.CharField(required=True, write_only=True)
    uidb64 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs:dict) -> dict:
        """Validate uidb64, token, and the new password to update the users password."""
        try:
            uid = smart_str(urlsafe_base64_decode(attrs.get('uidb64', '')))
            
            user = User.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user, attrs.get('token')):
                raise AuthenticationFailed('The reset token is invalid', "401")
            user.set_password(attrs.get('password'))
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset token is invalid', "401")
        return super().validate(attrs)


