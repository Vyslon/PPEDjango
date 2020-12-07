from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# HTTP Codes tests :


class HomePageTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_index_page_not_connected_redirection(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 302)

    def test_index_page_connected(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)


class ConnectionTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_user_is_connected(self):
        self.client.login(username='temporary', password='temporary')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_user_is_not_connected_with_wrong_password(self):
        self.client.login(username='temporary', password='wrongpassword')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_is_not_connected_without_password(self):
        self.client.login(username='temporary')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
