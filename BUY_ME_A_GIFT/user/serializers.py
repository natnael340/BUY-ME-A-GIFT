from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
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
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')
        
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'])
        
        return user
        
class PasswordResetSerializer(serializers.Serializer):     
    email = serializers.EmailField(required=True)    

    def validate(self, attrs):
        try:
            email = attrs.get('email', '')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator.make_token(uidb64)
                current_site = get_current_site(self.context.get('request')).domain
                relativeUrl = reverse('password_reset', kwargs={'token': token})
                absoluteUrl = f'http://{current_site}/{relativeUrl}'.format(current_site, relativeUrl)
                email_body  = f"Hello, \n Here is your password reset url {absoluteUrl}".format(url=absoluteUrl)
                data = {"email_body": email_body, 'to_email': user.email, 'email_subject': 'Reset Password'}
                
                Util.send_email(data)
            return attrs
        except expressions as indetifier:
            pass
        return super().validate(attrs)