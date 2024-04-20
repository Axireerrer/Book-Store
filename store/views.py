from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from store.permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet


from store.models import Book, UserBookRelation
from store.serializers import BookSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):

    queryset = Book.objects.all().annotate(
            annotate_likes=Count(Case(When(
             userbookrelation__like=True, then=1)))).order_by('id').select_related('owner').prefetch_related('readers')
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookAPI(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                              book_id=self.kwargs['book'])
        print('created', created)
        return obj


def auth(request):
    return render(request, 'oauth_github.html', context={'title': 'GitHub'})




