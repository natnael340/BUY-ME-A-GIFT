from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            password='testpass'
        )

    def test_user_creation(self) -> None:
        self.assertEqual(str(self.user.id), str(self.user.pk))
        self.assertEqual(self.user.email, 'testuser@test.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)
        self.assertTrue(self.user.check_password('testpass'))

    def test_create_superuser(self) -> None:
        superuser = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='adminpass'
        )
        self.assertTrue(superuser.is_admin)