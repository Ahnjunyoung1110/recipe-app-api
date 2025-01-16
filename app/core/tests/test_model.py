
# 모델 테스트
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    #모델 테스트

    def test_create_user_with_email_successful(self):
        #성공적인 경우 테스트
        email = 'test@example.com'
        password = 'test12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))