from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import PasswordResetForm

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
        self.cleaned_data = super().validate(attrs)
        form = PasswordResetForm(self.cleaned_data)
        if form.is_valid():
            return attrs
        raise serializers.ValidationError(form.errors) 