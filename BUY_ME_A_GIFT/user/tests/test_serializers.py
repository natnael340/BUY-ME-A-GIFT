"""
This module contains test cases and tests for user models.

It check the validity and integrity of the models.

"""

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
    """
    This test case checks that if a user can authenticate with the correct credentials

    """
    def setUp(self):
        """
        Set up the test case.

        This method create a user object for performing tests
        and initialize the serializer that serializes the user
        data for loging functionality

        """
        self.user = User.objects.create_user(
        email='test@test.com',
        password='testpass123'
        )
        self.serializer = UserLoginSerializers()

    def test_validate(self):
        """
        This method checks that the user can authenticate
        with the required arguments

        arguments: 
         - email: The user's email
         - password: The user's password
        
        Raises Error if the user cannot authenticate with the correct
        credentials
        """
        data = {'email': 'test@test.com', 'password': 'testpass123'}
        serializer = UserLoginSerializers(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['email'], 'test@test.com')
        

    def test_validate_invalid_email(self):
        """
        This test checks that if the user can authenticate with out
        providing a valid email address

        arguments: 
         - email: invalid email address
         - password: The user's password
        
        Raises exception if the user can authenticate with an invalid email
        """
        validated_data = {'email': 'invalidemail@test.com', 'password': 'testpass123'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(validated_data)

    def test_validate_invalid_password(self):
        """
        This test checks that if the user can authenticate with out
        providing a valid password

        arguments: 
         - email: The user's email
         - password: invalid password
        
        Raises exception if the user can authenticate with an invalid password
        """
        validated_data = {'email': 'test@test.com', 'password': 'invalidpassword'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(validated_data)

    def test_validate_missing_email(self):
        """
        This test checks that if the user can authenticate with out
        providing an email address

        arguments: 
         - password: The user's password
        
        Raises exception if the user can authenticate without an email
        """
        data = {'password': 'testpass123'}
        serializer = UserLoginSerializers(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_missing_password(self):
        """
        This test checks that if the user can authenticate with out
        providing an password

        arguments: 
         - email: The user's email address
        
        Raises exception if the user can authenticate without a password
        """
        data = {'email': 'test@test.com'}
        serializer = UserLoginSerializers(data=data)
        self.assertFalse(serializer.is_valid())

class UserRegisterSerializersTest(TestCase):
    """
    This test case checks that User objects can be created with the expected
    attributes, and that superusers can be created with the is_admin flag set
    to True.

    """
    def setUp(self):
        """
        Set up the test case.
        
        This method initializes the serializer to serialize the
        user data for registering functionality
        """
        self.serializer = UserRegisterSerializers()

    def test_create(self):
        """
        Test that a User object can be created with the expected attributes.

        This method checks that the User object has the expected email, password 
        attributes.
        """
        user_data = {'email': 'test@test.com', 'password': 'testpass123'}
        result = self.serializer.create(user_data)
        self.assertEqual(result.email, 'test@test.com')
        self.assertTrue(result.check_password('testpass123'))

    def test_create_existing_email(self):
        """
        Test that a User object can be created with the duplicate email address.
        
        This method checks that an account can't be created with a duplicate email 
        attributes.
        """
        User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        user_data = {'email': 'test@test.com', 'password': 'testpass123'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.create(user_data)

    def test_missing_email(self):
        """
        Test that a User object can be created with out email address.
        
        This method checks that an account can't be created with out an email 
        attributes.
        """
        data = {'password': 'testpass123'}
        serializer = UserRegisterSerializers(data=data)
        self.assertFalse(serializer.is_valid())

    def test_missing_password(self):
        """
        Test that a User object can be created with out email address.
        
        This method checks that an account can't be created with out a password.
        attributes.
        """
        data = {'email': 'test@test.com'}
        serializer = UserRegisterSerializers(data=data)
        self.assertFalse(serializer.is_valid())

class PasswordResetSerializerTest(TestCase):
    """
    This test case checks that Password Reset Token can be generated with required
    attributes, and that They can be sent to the email adress of the user.

    """
    def setUp(self):
        """
        Set up the test case.
        
        This method initializes the serializer to serialize the
        user data for registering functionality
        
        Also it creates a user object
        """
        self.serializer = PasswordResetSerializer()
        self.user = User.objects.create_user(
        email='test@test.com',
        password='testpass123'
        )

    def test_validate_invalid_email(self):
        """
        This method checks if token can be generated with invalid email address
        """
        validated_data = {'email': 'invalidemail@test.com'}
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(validated_data)

    def test_validate_missing_email(self):
        """
        This method checks if token can be generated with out providing email address
        """
        data = {}
        serializer = UserRegisterSerializers(data=data)
        self.assertFalse(serializer.is_valid())

class SetNewPasswordSerializerTest(TestCase):
    """
    Test cases for the Reset the user password given the 
    uid and token class.
    """
    def setUp(self):
        """
        Set Up the Test Case

        This method is crate instance for serializing the income data.
        Also creates a new User object

        """
        self.serializer = SetNewPasswordSerializer()
        self.user = User.objects.create_user(
        email='test@test.com',
        password='testpass123'
        )
        self.uid = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_validate(self):
        """
        This method checks if password can be reset with valid 
        token and uid of the user
        """
        validated_data = {'password': 'newpass123', 'uidb64': self.uid, 'token': self.token}
        result = self.serializer.validate(validated_data)
        self.assertEqual(result, validated_data)

    def test_validate_invalid_token(self):
        """
        The method check if password can be set with invalid token.
        """
        validated_data = {'password': 'newpass123', 'uidb64': self.uid, 'token': 'invalidtoken'}
        with self.assertRaises(AuthenticationFailed):
            self.serializer.validate(validated_data)

    def test_validate_invalid_uidb64(self):
        """
        The method check if password can be set with invalid user id.
        """
        validated_data = {'password': 'newpass123', 'uidb64': 'invaliduidb64', 'token': self.token}
        with self.assertRaises(AuthenticationFailed):
            self.serializer.validate(validated_data)

    def test_validate_missing_password(self):
        """
        The method check if password can be set with out password parameter.
        """
        data = {'uidb64': self.uid, 'token': self.token}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_missing_uidb64(self):
        """
        The method check if password can be set with out user id.
        """
        data = {'password': 'newpass123', 'token': self.token}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_validate_missing_token(self):
        """
        The method check if password can be set with out token.
        """
        data = {'password': 'newpass123', 'uidb64': self.uid}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
