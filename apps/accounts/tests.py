from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.conf import settings


User = get_user_model()


class TestAuthViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpass123'
        )
        self.password = 'testpass123'
        self.login_url = reverse(getattr(settings, 'LOGIN_URL'))
        self.logout_url = reverse('accounts:logout')

    def test_user_exists(self):
        self.assertEqual(self.user, User.objects.get(username='testuser'))
        self.assertFalse(self.user.email_verified)

    def test_user_login(self):
        logged_in = self.client.login(
            username=self.user.username,
            password=self.password
        )

        user = get_user(self.client)

        self.assertTrue(logged_in)
        self.assertNotEqual(type(user), AnonymousUser)

    def test_user_login_with_username(self):
        response = self.client.post(
            self.login_url,
            data={
                'username': self.user.username,
                'password': self.password,
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_user_login_with_email(self):
        response = self.client.post(
            self.login_url,
            data={
                'username': self.user.email,
                'password': self.password,
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_user_logout(self):
        self.client.post(
            self.login_url,
            data={
                'username': self.user.username,
                'password': self.password,
            },
            follow=True
        )

        response = self.client.post(
            self.logout_url,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertEqual(type(get_user(self.client)), AnonymousUser)
