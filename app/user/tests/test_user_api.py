from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users public API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'yo@gloubiboulga.com',
            'password': 'whatever',
            'name': 'Bertrand Cheu'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        print(res)

        # Make sure the API returns successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Make sure the password is the one we set
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        # Make sure the password is NOT in the returned data
        self.assertNotIn('password', res.data)

    def test_user_already_exists(self):
        """Test if the user already exists"""
        payload = {
            'email': 'yo@gloubiboulga.com',
            'password': 'whatever'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_complies(self):
        """Test that the password complies"""
        payload = {
            'email': 'yo@gloubiboulga.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'gobi@gloubiboulga.com',
            'password': 'whatever'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created with invalid credentials"""
        payload = {
            'email': 'gobi@gloubiboulga.com',
            'password': 'wrongpassword'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that a token is not created when user does not exist"""
        payload = {
            'email': 'gobi@gloubiboulga.com',
            'password': 'whatever'
        }

        # Note that we do NOT create the user in this case
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {
            'email': 'yo@gloubiboulga.com',
            'password': ''
        }

        # Note that we do NOT create the user in this case either
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
