from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Card, Board, List, Comment, Label
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class CardAPITests(APITestCase):
    '''Test case for cards'''
    def setUp(self):
        #test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        #getting JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.board = Board.objects.create(title="Test board", owner=self.user, is_public=False)
        self.list = List.objects.create(title='Test list', board=self.board)
    
    def test_get_cards(self):
        #authorized get request fo cards
        Card.objects.create(title='Task1', list=self.list, priority='LOW')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/cards/')
        #checking
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task1')
        self.assertEqual(response.data[0]['priority'], 'LOW')
    
    def test_create_card(self):
        #authorized post request fo cards
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'title': 'New Task',
            'description': 'Test task',
            'list': self.list.id,
            'priority': 'MEDIUM',
            'order': 1
        }
        response = self.client.post('/api/cards/', data, format='json')
        #checking
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get(title='New Task').title, 'New Task')
        self.assertEqual(response.data['priority'], 'MEDIUM')

    def test_create_card_unauth(self):
        #unauthorized post request fo cards
        data = {
            'title': 'Unauth task',
            'list': self.list.id,
            'priority': 'HIGH'
        }
        response = self.client.post('/api/cards/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_with_invalid_priority(self):
        #creating task with invalid priority data
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            'title': 'Task wrong prio',
            'list': self.list.id,
            'priority': 'INVALID'
        }
        responce = self.client.post('/api/cards/', data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('priority', responce.data)
