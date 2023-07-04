from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            first_name="Jack", last_name="Doe", email="user@mail.com", password="123"
        )
        self.assertEqual(user.email, "user@mail.com")
        self.assertNotEqual(user.email, "wrong@mail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="Jack", last_name="Doe", email="", password="123"
            )

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            first_name="Jane", last_name="Doe", email="admin@mail.com", password="123"
        )
        self.assertEqual(superuser.email, "admin@mail.com")
        self.assertNotEqual(superuser.email, "wrong@mail.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertIsNone(superuser.username)

        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(TypeError):
            User.objects.create_superuser(email="")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                first_name="", last_name="Doe", email="admin@mail.com", password="123"
            )
