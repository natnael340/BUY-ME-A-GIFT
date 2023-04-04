"""
This module contains test cases for views related to 
authentication and authorization.

It contain endpoint test for user login, user registration and 
password reset.
"""
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework import status
from user.views import (
    LoginView,
    SignUpView,
    PasswordResetView,
    SetNewPasswordApiView,
    PasswordResetTokenCheckView
)
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class LoginViewTest(TestCase):
    """
    Test case fo user login
    """
    def setUp(self) -> None:
        """
        Set up the test case.

        Create a user object wich will be used to test the login
        """
        self.factory = RequestFactory()
        user = User.objects.create(email="abcd@gmail.com")
        user.set_password("password")
        user.save()

    def test_login_view_with_correct_credentials(self) -> None:
        """
        This test check if a user can login with correct credentials

        Request Data:
         - email: valid user email
         - password: valid user password
        """
        data = {
            "email": "abcd@gmail.com",
            "password": "password"
        }
        request=self.factory.post(reverse('login'), data=data, format='json')

        response = LoginView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view_with_incorrect_credentials(self) -> None:
        """
        This test check if a user can login with incorrect credentials

        Request Data:
         - email: valid user email 
         - password: invalid user password
        """
        data = {
            "email": "abcd@gmail.com",
            "password": "passwor2"
        }
        request=self.factory.post(reverse('login'), data=data, format='json')

        response = LoginView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_view_with_incomplete_credentials(self) -> None:
        """
        This test check if a user can login with only email addresses

        Request Data:
         - email: valid user email
        """
        data = {
            "email": "abcd@gmail.com"
        }
        request=self.factory.post(reverse('login'), data=data, format='json')

        response = LoginView.as_view()(request)
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SignUpViewTestCase(TestCase):
    """
    Test Case for user registration
    """
    def setUp(self) -> None:
        """
        Set up the test case.

        1. Create a user object wich will be used to test the duplicate registration
        2. Create a factory instance to make requests to the view
        """
        self.factory = RequestFactory()
        user = User.objects.create(email="testuser@example.com")
        user.set_password("password")
        user.save()
    
    def test_sign_up_view(self) -> None:
        """
        This method is test if a user can be registered with valid
        email and password

        Request Data:
         - email: valid email
         - password: valid password
        """
        user = {
            "email": "user@example.com",
            "password": "password"
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(email=user["email"]).exists(), True)

    def test_sign_up_view_with_invalid_password(self) -> None:
        """
        This method is test if a user can be registered with valid
        email and invalid password like empty password

        Request Data:
         - email: valid email
         - password: empty password
        """
        user = {
            "email": "user@example.com",
            "password": ""
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_sign_up_view_with_invalid_email(self) -> None:
        """
        This method is test if a user can be registered with invalid
        email and valid password

        Request Data:
         - email: invalid email address
         - password: valid password
        """
        user = {
            "email": "user@.com",
            "password": "password"
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_view_with_same_email(self) -> None:
        """
        This method test if a user can be registered with existing
        user email address

        Request Data:
         - email: existing user email address
         - password: valid password
        """
        user = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetViewTestCase(TestCase):
    """
    Test cases for resetting user password
    """
    def setUp(self) -> None:
        """
        Set up the test case.

        1. Create a user object wich will be used to test for password reset
        2. Create a factory instance to make requests to the view
        """
        self.factory = RequestFactory()
        user = User.objects.create(email="testuser@example.com")
        user.set_password("password")
        user.save()

    def test_create_a_password_reset_token(self) -> None:
        """
        This method tests if a password reset token can be generated
        for a valid user email

        Request Data:
         - email: existing user email address
        """
        data = {
            "email": "testuser@example.com"
        }
        request=self.factory.post(reverse('reset'), data=data, format='json')
        response = PasswordResetView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_password_reset_token_with_invalid_email(self) -> None:
        """
        This method tests if a password reset token can be generated
        for a invalid user email

        Request Data:
         - email: unregistered user email
        """
        data = {
            "email": "testuseraaa@example.com"
        }
        request=self.factory.post(reverse('reset'), data=data, format='json')
        response = PasswordResetView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PasswordResetTokenCheckViewTestCase(TestCase):
    """
    Test cases for check if password reset token is valid
    """
    def setUp(self) -> None:
        """
        Set up the test case.

        1. Create a user object wich will be used to test for password reset
        2. Generate a new password reset token for the created user
        3. Generate base64 encoded uidb64 from user id
        4. Create a factory instance to make requests to the view
        """
        self.factory = RequestFactory()
        self.user = User.objects.create(email="testuser@example.com")
        self.user.set_password("password")
        self.user.save()
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
    
    def test_check_if_token_is_valid(self) -> None:
        """
        This method tests if a token is valid given a base64 encoded 
        user id string and a valid token

        Request Data:
         - token: generated password reset token
         - uidb64: base64 encoded user id
        """
        request = self.factory.get(reverse('password_reset', kwargs={'token': self.token, 'uidb64': self.uidb64}))
        response = PasswordResetTokenCheckView.as_view()(request, uidb64=self.uidb64, token=self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_if_token_is_valid_with_invalid_token(self) -> None:
        """
        This method tests if a token is valid given a base64 encoded 
        user id string and an invalid token

        Request Data:
         - token: invalid token
         - uidb64: base64 encoded user id
        """
        request = self.factory.get(reverse('password_reset', kwargs={'token': "badaea", 'uidb64': self.uidb64}))
        response = PasswordResetTokenCheckView.as_view()(request, uidb64="badaea", token=self.token)

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_if_other_user_password_can_be_changed_with_other_user_token(self) -> None:
        """
        This method tests if a valid generated token for user A can 
        reset the password of user B using the user id of the user B
        insead of user A.

        Request Data:
         - token: generated password reset token for user A
         - uidb64: base64 encoded user id of user B
        """
        other_user = User.objects.create(email="otheruser@example.com")
        other_user.set_password("otherpassword")
        other_user.save()
        other_uidb64 = urlsafe_base64_encode(smart_bytes(other_user.id))
        other_token = PasswordResetTokenGenerator().make_token(other_user)

        request = self.factory.get(reverse('password_reset', kwargs={'token': other_token, 'uidb64': self.uidb64}))
        response = PasswordResetTokenCheckView.as_view()(request, uidb64=self.uidb64, token=other_token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
class PasswordResetWithTokenViewTestCase(TestCase):
    """
    Test cases for resetting user password
    """
    def setUp(self) -> None:
        """
        Set up the test case.

        1. Create a user object wich will be used to change the password
        2. Generate a new password reset token for the created user
        3. Generate base64 encoded uidb64 from user id
        4. Create a factory instance to make requests to the view
        """
        self.factory = RequestFactory()
        self.user = User.objects.create(email="testuser@example.com")
        self.user.set_password("password")
        self.user.save()
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_reset_password_with_valid_token(self) -> None:
        """
        Test if a user password can be reset with a valid token, 
        a valid user id and a valid password.
        
        Request Data:
         - token: generated password reset token
         - uidb64: base64 encoded user id
         - password: new password
        """
        data = {
            "password": "newpassword",
            "uidb64": str(self.uidb64),
            "token": str(self.token)
        }
        str_data = json.dumps(data)
        request=self.factory.patch(reverse('password_reset_done'), data=str_data, content_type='application/json')
        response = SetNewPasswordApiView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_reset_password_with_invalid_token(self) -> None:
        """
        Test if a user password can be reset with a invalid token, 
        a valid user id and a valid password.
        
        Request Data:
         - token: invalid password reset token
         - uidb64: base64 encoded user id
         - password: new password
        """
        data = {
            "password": "newpassword",
            "uidb64": str(self.uidb64),
            "token": "axaca"
        }
        str_data = json.dumps(data)
        request=self.factory.patch(reverse('password_reset_done'), data=str_data, content_type='application/json')
        response = SetNewPasswordApiView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_reset_password_with_other_user_token(self) -> None:
        """
        Test if a user A password can be reset with User B valid token, 
        by using user A user id as uid.
        
        Request Data:
         - token: generated password reset token for user B
         - uidb64: base64 encoded user id of user A
         - password: new password
        """
        other_user = User.objects.create(email="otheruser@example.com")
        other_user.set_password("otherpassword")
        other_user.save()
        other_uidb64 = urlsafe_base64_encode(smart_bytes(other_user.id))
        other_token = PasswordResetTokenGenerator().make_token(other_user)
        data = {
            "password": "newpassword",
            "uidb64": str(self.uidb64),
            "token": str(other_token)
        }
        str_data = json.dumps(data)
        request=self.factory.patch(reverse('password_reset_done'), data=str_data, content_type='application/json')
        response = SetNewPasswordApiView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)