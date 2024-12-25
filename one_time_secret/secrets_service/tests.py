import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "one_time_secret.config.settings")

django.setup()

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from .models import Secret
from django.utils.crypto import get_random_string
import json


class SecretTestCase(TestCase):
    def test_generate_secret(self):
        response = self.client.post(reverse('generate_secret'), data=json.dumps({
            "secret": "This is a test secret.",
            "passphrase": "testpassphrase"
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('secret_key', response.json())

    def test_get_secret(self):
        secret = Secret.objects.create(secret_key="testkey", secret="This is a test secret.", passphrase="testpassphrase")
        response = self.client.get(reverse('get_secret', args=[secret.secret_key]), data={'passphrase': 'testpassphrase'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('secret', response.json())

class SecretServiceTests(TestCase):
    def setUp(self): #Создание тестового секркта
        self.secret_key = get_random_string(64)
        self.secret = 'This is a test secret'
        self.passphrase = 'test_passphrase'
        self.secret_obj = Secret.objects.create(
            secret_key=self.secret_key,
            secret=self.secret,
            passphrase=self.passphrase
        )

    def test_get_secret_success(self): #Успешное получение секрета
        response = self.client.get(
            reverse('get_secret', args=[self.secret_key]),
            {'passphrase': self.passphrase}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'secret': self.secret})

    def test_get_secret_deletion_after_access(self): #Проверка удаления секрета после 1 вызова
        # Первый запрос успешно получает секрет
        response = self.client.get(
            reverse('get_secret', args=[self.secret_key]),
            {'passphrase': self.passphrase}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'secret': self.secret})

        # Повторный запрос должен вернуть 404
        response = self.client.get(
            reverse('get_secret', args=[self.secret_key]),
            {'passphrase': self.passphrase}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Secret not found.'})

    def test_get_secret_incorrect_passphrase(self):
        response = self.client.get(
            reverse('get_secret', args=[self.secret_key]),
            {'passphrase': 'wrong_passphrase'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'error': 'Incorrect passphrase.'})

    def test_get_secret_expired_secret(self): #Проверка автоудаления
        self.secret_obj.expires_at = self.secret_obj.created_at #Устанавливаем время создания секрета
        self.secret_obj.save()

        response = self.client.get(
            reverse('get_secret', args=[self.secret_key]),
            {'passphrase': self.passphrase}
        )
        self.assertEqual(response.status_code, 410)
        self.assertEqual(response.json(), {'error': 'This secret has expired.'})

