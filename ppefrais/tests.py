from django.test import TestCase, Client
from django.contrib.auth.models import User
from ppefrais.models import Utilisateur
from django.urls import reverse
from django.contrib import auth

# HTTP Codes tests :


class IndexPageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary',
                                             'temporary@gmail.com', 'temporary')
        Utilisateur.objects.create(user=self.user, statut="Visiteur", adresse="Adresse")

    def test_index_page(self):
        response = self.client.get(reverse('ppefrais:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_connected(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('ppefrais:index'))
        self.assertEqual(response.status_code, 302)


class HomePageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary',
                                             'temporary@gmail.com', 'temporary')
        Utilisateur.objects.create(user=self.user, statut="Visiteur", adresse="Adresse")

    def test_home_page(self):
        response = self.client.get(reverse('ppefrais:home'))
        self.assertEqual(response.status_code, 302)

    def test_home_page_connected(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('ppefrais:home'))
        self.assertEqual(response.status_code, 200)


class ConnectionTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary',
                                             'temporary@gmail.com', 'temporary')

    def test_user_is_connected(self):
        password = 'temporary'
        username = 'temporary'
        response = self.client.post(reverse(
            'ppefrais:index'), {
                'username': username,
                'password': password,
            })
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
