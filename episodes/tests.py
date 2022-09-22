from django.test import TestCase

from users.models import User


class TaskTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='test', password='12test12', email='test@example.com'
        )

    def test_check_user(self):
        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test1')
