from django.contrib.auth.hashers import check_password
from django.test import SimpleTestCase, TestCase

from {{ cookiecutter.project_slug }}.user_auth.models import User
from {{ cookiecutter.project_slug }}.user_auth.tests import factories


class UserManagerTests(TestCase):
    def test_create_user(self):
        User.objects.create_user("test@example.com", "password")

        user = User.objects.get()

        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(check_password("password", user.password))

    def test_create_user_no_email(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user(None, "password")

    def test_create_superuser(self):
        User.objects.create_superuser("test@example.com", "password")

        user = User.objects.get()

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(check_password("password", user.password))

    def test_create_superuser_is_staff_false(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                "test@example.com", "password", is_staff=False
            )

    def test_create_superuser_is_superuser_false(self):
        with self.assertRaisesMessage(
            ValueError, "Superuser must have is_superuser=True."
        ):
            User.objects.create_superuser(
                "test@example.com", "password", is_superuser=False
            )


class UserTests(SimpleTestCase):
    def test___str__(self):
        user = factories.User.build(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")
