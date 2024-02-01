from django.test import TestCase
from users.models import User
from .models import Stake

class PlaceStakeTestCase(TestCase):
    '''
    Test the act of placing a Bet on the site    
    '''
    def setUp(self):      
        self.user = User.objects.create(username="0710001000", email="testa@gmail.com")  

    def test_successfull_user_has_place_a_bet(self):
        self.assertEqual(2, 3)
        self.assertEqual(8, 8)

