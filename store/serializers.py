from rest_framework import serializers
from store.models import Book, UserBookRelation, User


class ReadersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):

    annotate_likes = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True, default="")
    readers = ReadersSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author_name', 'annotate_likes', 'rating', 'owner_name', 'readers']


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']


