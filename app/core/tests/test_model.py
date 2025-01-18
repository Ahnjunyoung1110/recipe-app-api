
# 모델 테스트
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    # 모델 테스트

    def test_create_user_with_email_successful(self):
        # 성공적인 경우 테스트
        email = 'test@example.com'
        password = 'test12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # 이메일의 변경을 테스트
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]  # 도메인은 대문자가 될 수 없다. 그래서 변경

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        # 빈칸 오면 에러 테스트
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        # SP생성 테스트
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
