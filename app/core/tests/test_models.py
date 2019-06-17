from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successfull"""
        email = 'test@londonappdev.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalised"""
        email = 'test@GLOUBIBOULGA.com'
        user = get_user_model().objects.create_user(email, 'whatever')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user without an email generates an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'whatever')

    def test_create_new_super_user(self):
        """Creating new super user"""
        user = get_user_model().objects.create_superuser(
            'test@gloubiboulgo.fr',
            'somepassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
