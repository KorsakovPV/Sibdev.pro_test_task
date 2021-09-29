from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.factories import AccountFactory
from priorities.factories import PrioritiesNameModelFactory, PrioritiesModelFactory


class MethodConformanceTestCase(APITestCase):

    def setUp(self):
        self.account1 = AccountFactory(confirmed=True)
        self.token = RefreshToken.for_user(self.account1)
        self.account2 = AccountFactory(confirmed=True)
        self.account3 = AccountFactory(confirmed=True)
        self.priorities1 = PrioritiesNameModelFactory(name='предпочтение1')
        self.priorities2 = PrioritiesNameModelFactory(name='предпочтение2')
        self.priorities3 = PrioritiesNameModelFactory(name='предпочтение3')
        self.priorities4 = PrioritiesNameModelFactory(name='предпочтение4')
        self.priorities5 = PrioritiesNameModelFactory(name='предпочтение5')

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_1(self):
        # Запрос аутентифицированного пользователя. Предпочтения не указаны.
        request_data = {}
        url = reverse('priorities:prioritiesmodel-compatibility-list')
        response = self.client.get(url, request_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, [])

    def test_2(self):
        # Запрос аутентифицированного пользователя. Предпочтения совпадают на 100% и 75%. В выводе 2 человека.
        self.account1_priorities1 = PrioritiesModelFactory(account=self.account1, priorities_name=self.priorities1, importance=10)
        self.account2_priorities1 = PrioritiesModelFactory(account=self.account2, priorities_name=self.priorities1, importance=10)
        self.account3_priorities1 = PrioritiesModelFactory(account=self.account3, priorities_name=self.priorities1, importance=5)
        request_data = {}
        url = reverse('priorities:prioritiesmodel-compatibility-list')
        response = self.client.get(url, request_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), 2)
        self.assertEqual(response_content[0].get('conformance'), 100)
        self.assertEqual(response_content[1].get('conformance'), 75)
        self.account1_priorities1.delete()
        self.account2_priorities1.delete()
        self.account3_priorities1.delete()

    def test_3(self):
        # Запрос аутентифицированного пользователя. Предпочтения совпадают на 100% и 50%. В выводе 1 человека.
        self.account1_priorities1 = PrioritiesModelFactory(account=self.account1, priorities_name=self.priorities1, importance=10)
        self.account2_priorities1 = PrioritiesModelFactory(account=self.account2, priorities_name=self.priorities1, importance=10)
        self.account3_priorities1 = PrioritiesModelFactory(account=self.account3, priorities_name=self.priorities1, importance=0)
        request_data = {}
        url = reverse('priorities:prioritiesmodel-compatibility-list')
        response = self.client.get(url, request_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), 1)
        self.assertEqual(response_content[0].get('conformance'), 100)
        self.account1_priorities1.delete()
        self.account2_priorities1.delete()
        self.account3_priorities1.delete()

    def tearDown(self):
        self.priorities1.delete()
        self.priorities2.delete()
        self.priorities3.delete()
        self.priorities4.delete()
        self.priorities5.delete()
        self.account1.delete()
        self.account2.delete()
        self.account3.delete()
