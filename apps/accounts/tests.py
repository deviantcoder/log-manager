from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_user_exists(self):
        self.assertEqual(self.user, User.objects.get(username='testuser'))
