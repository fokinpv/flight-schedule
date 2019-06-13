from django.test import TestCase
from apps.users.models import User

class UserTest(TestCase):

    def setUp(self):

        test_user1 = User.objects.create(
            username='testuser1',
            email='testuser1@test.com'
        )

        test_user1.set_password('qwer1234')

        test_user2 = User.objects.create(
            username='testuser2',
            email='testuser2@test.com'
        )

        test_user1.set_password('1234qrew')

    def test_get_users(self):

        users = User.objects.all()
        self.assertEqual(len(users), 2)
        
          
        