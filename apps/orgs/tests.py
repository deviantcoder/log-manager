from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from .models import Organization


User = get_user_model()


class OrgTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
    
    def create_org(self, name='Test Org', description='Some text...', status=Organization.StatusChoices.ACTIVE):
        try:
            org = Organization.objects.create(
                name=name,
                description=description,
                owner=self.user,
                status=status,
            )

            return org
        except Exception as e:
            print('Error during org creation: ', e)
            raise

    def test_create_org(self):
        org = self.create_org()
        
        self.assertEqual(org.name, 'Test Org')
        self.assertEqual(org.owner, self.user)
        self.assertEqual(org.slug, slugify(org.name))

    def test_create_org_view(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('orgs:create_org'),
            data={
                'name': 'Test Org 2',
                'description': 'Some text...'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Organization.objects.filter(name='Test Org 2').exists())
        self.assertEqual(Organization.objects.get(name='Test Org 2').owner, self.user)

    def test_delete_org_view(self):
        self.client.force_login(self.user)

        org = self.create_org()

        response = self.client.post(
            reverse('orgs:delete_org_confirm', kwargs={'id': org.pk}),
            data={
                'password': 'testpass123',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Organization.DoesNotExist):
            Organization.objects.get(name='Test Org')

    def test_change_org_status(self):
        self.client.force_login(self.user)

        org = self.create_org()

        response = self.client.post(
            reverse('orgs:change_org_status', kwargs={'id': org.pk}),
            data={
                'status': Organization.StatusChoices.INACTIVE
            },
            follow=True
        )

        org.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(org.status, Organization.StatusChoices.INACTIVE)

    def test_orgs_with_same_name_have_different_slugs(self):
        org1 = self.create_org()
        org2 = self.create_org()

        self.assertNotEqual(org1.slug, org2.slug)

    def test_org_status_filter(self):
        self.client.force_login(self.user)

        org = self.create_org(status=Organization.StatusChoices.ACTIVE)
        org = self.create_org(status=Organization.StatusChoices.INACTIVE)
        org = self.create_org(status=Organization.StatusChoices.ARCHIVED)

        # active check

        GET_PARAMS = {'org_status': Organization.StatusChoices.ACTIVE}
        response = self.client.get(reverse('orgs:orgs_list'), GET_PARAMS)

        qs = response.context.get('filter').qs

        for org in qs:
            self.assertEqual(org.status, Organization.StatusChoices.ACTIVE)

        # inactive check

        GET_PARAMS = {'org_status': Organization.StatusChoices.INACTIVE}
        response = self.client.get(reverse('orgs:orgs_list'), GET_PARAMS)

        qs = response.context.get('filter').qs

        for org in qs:
            self.assertEqual(org.status, Organization.StatusChoices.INACTIVE)

        # archived check

        GET_PARAMS = {'org_status': Organization.StatusChoices.ARCHIVED}
        response = self.client.get(reverse('orgs:orgs_list'), GET_PARAMS)

        qs = response.context.get('filter').qs

        for org in qs:
            self.assertEqual(org.status, Organization.StatusChoices.ARCHIVED)
