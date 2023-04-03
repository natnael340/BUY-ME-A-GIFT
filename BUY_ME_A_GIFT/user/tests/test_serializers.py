import uuid
from django.test import TestCase
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from user.models import User
from user.serializers import UserLoginSerializers, UserRegisterSerializers, PasswordResetSerializer, SetNewPasswordSerializer
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import  urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
from unittest.mock import Mock, MagicMock


class UserLoginSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        email='test@test.com',
        password='testpass123'
        )
        self.serializer = UserLoginSerializers()

    def test_validate(self):
        data = {'email': 'test@test.com', 'password': 'testpass123'}
        serializer = UserLoginSerializers(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['email'], 'test@test.com')
        

    def test_validate_invalid_email(self):
        validated_data = {'email': 'invalidemail@test.com', 'password': 'testpass123'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(validated_data)

    def test_validate_invalid_password(self):
        validated_data = {'email': 'test@test.com', 'password': 'invalidpassword'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(validated_data)

    def test_validate_missing_email(self):
        data = {'email': 'test@test.com'}
        serializer = UserLoginSerializers(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_missing_password(self):
        data = {'email': 'test@test.com'}
        serializer = UserLoginSerializers(data=data)
        self.assertFalse(serializer.is_valid())

class UserRegisterSerializersTest(TestCase):
    def setUp(self):
        self.serializer = UserRegisterSerializers()

    def test_create(self):
        user_data = {'email': 'test@test.com', 'password': 'testpass123'}
        result = self.serializer.create(user_data)
        self.assertEqual(result.email, 'test@test.com')
        self.assertTrue(result.check_password('testpass123'))

    def test_create_existing_email(self):
        User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        user_data = {'email': 'test@test.com', 'password': 'testpass123'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.create(user_data)

    def test_missing_email(self):
        data = {'password': 'testpass123'}
        serializer = UserRegisterSerializers(data=data)
        self.assertFalse(serializer.is_valid())

    def test_missing_password(self):
        data = {'email': 'test@test.com'}
        serializer = UserRegisterSerializers(data=data)
        self.assertFalse(serializer.is_valid())

class PasswordResetSerializerTest(TestCase):
    def setUp(self):
        self.serializer = PasswordResetSerializer()
        self.user = User.objects.create_user(
        email='test@test.com',
        password='testpass123'
        )

    def test_validate_invalid_email(self):
        validated_data = {'email': 'invalidemail@test.com'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(validated_data)

    def test_validate_missing_email(self):
        data = {}
        serializer = UserRegisterSerializers(data=data)
        self.assertFalse(serializer.is_valid())

class SetNewPasswordSerializerTest(TestCase):
    def setUp(self):
        self.serializer = SetNewPasswordSerializer()
        self.user = User.objects.create_user(
        email='test@test.com',
        password='testpass123'
        )
        self.uid = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_validate(self):
        validated_data = {'password': 'newpass123', 'uidb64': self.uid, 'token': self.token}
        result = self.serializer.validate(validated_data)
        self.assertEqual(result, validated_data)

    def test_validate_invalid_token(self):
        validated_data = {'password': 'newpass123', 'uidb64': self.uid, 'token': 'invalidtoken'}
        with self.assertRaises(AuthenticationFailed):
            self.serializer.validate(validated_data)

    def test_validate_invalid_uidb64(self):
        validated_data = {'password': 'newpass123', 'uidb64': 'invaliduidb64', 'token': self.token}
        with self.assertRaises(AuthenticationFailed):
            self.serializer.validate(validated_data)

    def test_validate_missing_password(self):
        data = {'uidb64': self.uid, 'token': self.token}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_missing_uidb64(self):
        data = {'password': 'newpass123', 'token': self.token}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_missing_token(self):
        data = {'password': 'newpass123', 'uidb64': self.uid}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
