from django.db.models import Count, Case, When, Avg

from store.serializers import BookSerializer
from django.test import TestCase
from store.models import Book, UserBookRelation, User


class BookSerializerTest(TestCase):

    def setUp(self):

        self.book_1 = Book.objects.create(name='Test Book 1', price=25, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test Book 2', price=55, author_name='Author 2')

        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=1)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True, rate=5)

        UserBookRelation.objects.create(user=user1, book=self.book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=self.book_2, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book_2, like=False, rate=4)

    def test_ok(self):

        books = Book.objects.all().annotate(
            annotate_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')).order_by('id')

        serializer_data = BookSerializer(books, many=True).data

        expected_data = [

            {
                'id': self.book_1.id,
                'name': 'Test Book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'annotate_likes': 3,
                'rating': '3.33',
            },

            {
                'id': self.book_2.id,
                'name': 'Test Book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                'annotate_likes': 2,
                'rating': '4.00',
            }
        ]
        self.assertEqual(expected_data, serializer_data)
