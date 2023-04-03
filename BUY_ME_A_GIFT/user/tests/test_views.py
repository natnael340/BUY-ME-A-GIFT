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
    def setUp(self) -> None:
        self.factory = RequestFactory()
        user = User.objects.create(email="abcd@gmail.com")
        user.set_password("password")
        user.save()

    def test_login_view_with_correct_credentials(self) -> None:
        data = {
            "email": "abcd@gmail.com",
            "password": "password"
        }
        request=self.factory.post(reverse('login'), data=data, format='json')

        response = LoginView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view_with_incorrect_credentials(self) -> None:
        data = {
            "email": "abcd@gmail.com",
            "password": "passwor1"
        }
        request=self.factory.post(reverse('login'), data=data, format='json')

        response = LoginView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_view_with_incomplete_credentials(self) -> None:
        data = {
            "email": "abcd@gmail.com"
        }
        request=self.factory.post(reverse('login'), data=data, format='json')

        response = LoginView.as_view()(request)
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SignUpViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        user = User.objects.create(email="testuser@example.com")
        user.set_password("password")
        user.save()
    
    def test_sign_up_view(self) -> None:
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
        user = {
            "email": "user@example.com",
            "password": ""
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_sign_up_view_with_invalid_email(self) -> None:
        user = {
            "email": "user@.com",
            "password": ""
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_view_with_same_email(self) -> None:
        user = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        request=self.factory.post(reverse('signup'), data=user, format='json')
        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        user = User.objects.create(email="testuser@example.com")
        user.set_password("password")
        user.save()

    def test_create_a_password_reset_token(self) -> None:
        data = {
            "email": "testuser@example.com"
        }
        request=self.factory.post(reverse('reset'), data=data, format='json')
        response = PasswordResetView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_password_reset_token_with_invalid_email(self) -> None:
        data = {
            "email": "testuseraaa@example.com"
        }
        request=self.factory.post(reverse('reset'), data=data, format='json')
        response = PasswordResetView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PasswordResetTokenCheckViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(email="testuser@example.com")
        self.user.set_password("password")
        self.user.save()
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
    
    def test_check_if_token_is_valid(self) -> None:
        request = self.factory.get(reverse('password_reset', kwargs={'token': self.token, 'uidb64': self.uidb64}))
        response = PasswordResetTokenCheckView.as_view()(request, uidb64=self.uidb64, token=self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_if_token_is_valid_with_invalid_token(self) -> None:
        request = self.factory.get(reverse('password_reset', kwargs={'token': "badaea", 'uidb64': self.uidb64}))
        response = PasswordResetTokenCheckView.as_view()(request, uidb64="badaea", token=self.token)

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_if_other_user_password_can_be_changed_with_other_user_token(self) -> None:
        other_user = User.objects.create(email="otheruser@example.com")
        other_user.set_password("otherpassword")
        other_user.save()
        other_uidb64 = urlsafe_base64_encode(smart_bytes(other_user.id))
        other_token = PasswordResetTokenGenerator().make_token(other_user)

        request = self.factory.get(reverse('password_reset', kwargs={'token': other_token, 'uidb64': self.uidb64}))
        response = PasswordResetTokenCheckView.as_view()(request, uidb64=self.uidb64, token=other_token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
class PasswordResetWithTokenViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(email="testuser@example.com")
        self.user.set_password("password")
        self.user.save()
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_reset_password_with_valid_token(self) -> None:
        data = {
            "password": "newpassword",
            "uidb64": str(self.uidb64),
            "token": str(self.token)
        }
        data = json.dumps(data)
        request=self.factory.patch(reverse('password_reset_done'), data=data, content_type='application/json')
        response = SetNewPasswordApiView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_reset_password_with_invalid_token(self) -> None:
        data = {
            "password": "newpassword",
            "uidb64": str(self.uidb64),
            "token": "axaca"
        }
        data = json.dumps(data)
        request=self.factory.patch(reverse('password_reset_done'), data=data, content_type='application/json')
        response = SetNewPasswordApiView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_reset_password_with_other_user_token(self) -> None:
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
        data = json.dumps(data)
        request=self.factory.patch(reverse('password_reset_done'), data=data, content_type='application/json')
        response = SetNewPasswordApiView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)