from django.test import TestCase
from accounts.models import User

class CustomAccountManagerTests(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'strongpassword123',
        }

    def test_create_user_success(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)

    def test_create_user_without_password_raises(self):
        with self.assertRaisesMessage(ValueError, 'Password is requried'):
            User.objects.create_user(email='a@b.com', username='abc')

    def test_create_superuser_success(self):
        user = User.objects.create_superuser(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_create_superuser_is_staff_false_raises(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must be assigned is_staff = True'):
            User.objects.create_superuser(email='super@example.com', username='superuser', password='pass', is_staff=False)

    def test_create_superuser_is_superuser_false_raises(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must be assigned is_superuser = True'):
            User.objects.create_superuser(email='super@example.com', username='superuser', password='pass', is_superuser=False)

    def test_create_superuser_without_password_raises(self):
        with self.assertRaisesMessage(ValueError, 'Password is requried'):
            User.objects.create_superuser(email='super@example.com', username='superuser', password=None)

    def test_user_str_returns_email(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])
