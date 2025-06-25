from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.conf import settings


User = get_user_model()
login_url = getattr(settings, 'LOGIN_URL')


class TestUserLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpass123'
        )
        self.password = 'testpass123'
        self.login_url = reverse(login_url)
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


class TestUserLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpass123'
        )
        self.password = 'testpass123'
        self.login_url = reverse(getattr(settings, 'LOGIN_URL'))
        self.logout_url = reverse('accounts:logout')

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


class TestUserSignup(TestCase):
    def setUp(self):
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse(login_url)
        self.username = 'testuser'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.email = 'testuser@example.com'
        self.password = 'testpass123'

    def send_signup_request(
        self, email, username, first_name, last_name, password1, password2, follow=True
    ):
        response = self.client.post(
            self.signup_url,
            data={
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password1': password1,
                'password2': password2,
            },
            follow=follow
        )
        return response
    
    def test_user_signup(self):
        response = self.send_signup_request(
            self.email,
            self.username,
            self.first_name,
            self.last_name,
            self.password,
            self.password
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user(self.client), User.objects.get(username=self.username))
        self.assertTrue(get_user(self.client).is_authenticated)
