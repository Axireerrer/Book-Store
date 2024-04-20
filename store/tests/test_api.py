from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.utils import json

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BooksAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user2 = User.objects.create(username='test_user2', is_staff=True)
        self.book_1 = Book.objects.create(name='Test Book 1 Author 1', price=25, author_name='Author 3',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test Book 2', price=55, author_name='Author 2')
        self.book_3 = Book.objects.create(name='Test Book 3', price=65, author_name='Author 1')

        UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True, rate=5)

    def test_get(self):
        self.client.force_login(self.user)
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            annotate_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['annotate_likes'], 1)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotate_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        print(serializer_data, '\n\n', response.data)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('book-list')
        self.assertEqual(3, Book.objects.all().count())
        UserBookRelation.objects.create(user=self.user)
        data = {
            "name": "Hous of Knight",
            "price": 179.99,
            "author_name": 'Rolf Kainse',
            "likes_count": 0,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args={self.book_1.id})
        self.client.force_login(self.user)
        data = {
            "name": "Hous of Knight",
            "price": 99,
            "author_name": 'Rolf Kainse',
            "likes_count": 0,
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1 = Book.objects.get(id=self.book_1.id)
        self.assertEqual(99, self.book_1.price)

    def test_delete(self):
        url = reverse('book-detail', args={self.book_1.id})
        self.assertEqual(3, Book.objects.all().count())
        self.client.force_login(self.user)
        data = {
            "name": self.book_1.name,
            "price": self.book_1.price,
            "author_name": self.book_1.author_name,
            "likes_count": 0,
        }
        json_data = json.dumps(data)
        response = self.client.delete(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_update_not_owner_is_staff(self):
        url = reverse('book-detail', args={self.book_1.id})
        self.client.force_login(self.user2)
        data = {
            "name": "Hous of Knight",
            "price": 99,
            "author_name": 'Rolf Kainse',
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1 = Book.objects.get(id=self.book_1.id)
        self.assertEqual(99, self.book_1.price)


class BooksRelationAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user2 = User.objects.create(username='test_user2', is_staff=True)
        self.book_1 = Book.objects.create(name='Test Book 1 Author 1', price=25, author_name='Author 3',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test Book 2', price=55, author_name='Author 2')
        self.book_3 = Book.objects.create(name='Test Book 3', price=65, author_name='Author 1')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=[self.book_1.id])
        self.client.force_login(self.user)
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(relation.like)


