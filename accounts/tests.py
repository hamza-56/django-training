from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from todolist.models import TodoListItem

from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user-test-1',
                                 password='password1',
                                 first_name='user-1-first',
                                 last_name='user-1-last')
        User.objects.create_user(username='user-test-2',
                                 password='password2',
                                 first_name='user-2-first',
                                 last_name='user-2-last')

    def test_users_have_full_name(self):
        '''
        Ensure user's full name is correctly set
        '''
        user_1 = User.objects.get(username='user-test-1')
        user_2 = User.objects.get(username='user-test-2')
        self.assertEqual(user_1.full_name,
                         f'{user_1.first_name} {user_1.last_name}')
        self.assertEqual(user_2.full_name,
                         f'{user_2.first_name} {user_2.last_name}')


class ApiTest(APITestCase):
    def test_register_user(self):
        url = '/api/auth/register/'
        data = {'username': 'user-from-api', 'password': 'secret123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user-from-api')

    def test_register_user_without_password(self):
        url = '/api/auth/register/'
        data = {'username': 'user-from-api'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def get_access_token(self, username=None, password=None):
        url = '/api/token/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        return response.data['access']

    def test_get_auth_token(self):
        username = 'user-test-api'
        password = 'secret123'
        User.objects.create_user(username=username, password=password)
        self.get_access_token(username=username, password=password)

    def test_create_todo_without_login(self):
        data = {'title': 'title', 'due_date': '2021-07-27'}
        url = '/api/todos/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(TodoListItem.objects.count(), 0)

    def test_create_todo_with_login(self):
        username = 'user-test-api'
        password = 'secret123'
        user = User.objects.create_user(username=username, password=password)

        data = {'title': 'title', 'due_date': '2021-07-27'}
        url = '/api/todos/'

        token = self.get_access_token(username=username, password=password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoListItem.objects.count(), 1)

    def test_user_can_update_own_profile(self):
        username = 'user-test-api'
        password = 'secret123'
        profile_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'birth_date': '2020-07-27',
            'bio': 'bio bio bio',
        }
        user = User.objects.create_user(username=username, password=password)
        token = self.get_access_token(username=username, password=password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = f'/api/profile/{user.id}/'
        response = self.client.put(url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'],
                         profile_data['first_name'])
        self.assertEqual(response.data['last_name'], profile_data['last_name'])
        self.assertEqual(response.data['birth_date'],
                         profile_data['birth_date'])
        self.assertEqual(response.data['bio'], profile_data['bio'])

    def test_user_cant_update_other_profile(self):
        username1 = 'user-test-api-1'
        username2 = 'user-test-api-2'
        password = 'secret123'

        profile_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'birth_date': '2020-07-27',
            'bio': 'bio bio bio',
        }
        user1 = User.objects.create_user(username=username1, password=password)
        User.objects.create_user(username=username2, password=password)

        token = self.get_access_token(username=username2, password=password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = f'/api/profile/{user1.id}/'
        response = self.client.put(url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['first_name'],
                            profile_data['first_name'])
        self.assertNotEqual(response.data['last_name'],
                            profile_data['last_name'])
        self.assertNotEqual(response.data['birth_date'],
                            profile_data['birth_date'])
        self.assertNotEqual(response.data['bio'], profile_data['bio'])
