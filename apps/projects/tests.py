from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from .models import Project
from apps.orgs.models import Organization


User = get_user_model()


class TestProject(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

        self.org = Organization.objects.create(
            name='Test Org',
            owner=self.user
        )
    
    def test_create_project(self):
        project = Project.objects.create(
            org=self.org,
            name='Test Project',
            description='Some text...',
            created_by=self.user
        )
        
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.created_by, self.user)

    def test_create_project_view(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('projects:create_project'),
            data={
                'org': self.org.pk,
                'name': 'Test Project 2',
                'description': 'Some text...'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(name='Test Project 2').exists())
        self.assertEqual(Project.objects.get(name='Test Project 2').created_by, self.user)

    def test_delete_project_view(self):
        self.client.force_login(self.user)

        project = Project.objects.create(
            org=self.org,
            name='Test Project',
            created_by=self.user
        )

        response = self.client.post(
            reverse('projects:delete_project_confirm', kwargs={'id': project.pk}),
            data={
                'password': 'testpass123',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(name='Test Project')

    def test_change_project_status(self):
        self.client.force_login(self.user)

        project = Project.objects.create(
            org=self.org,
            name='Test Project',
            created_by=self.user
        )

        response = self.client.post(
            reverse('projects:change_project_status', kwargs={'id': project.pk}),
            data={
                'status': Project.StatusChoices.INACTIVE,
            },
            follow=True
        )

        project.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.status, Project.StatusChoices.INACTIVE)
