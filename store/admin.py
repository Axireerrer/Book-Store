from django.contrib import admin
from store.models import Book, UserBookRelation


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    ordering = ['id']
    pass


@admin.register(UserBookRelation)
class AdminUserBookRelation(admin.ModelAdmin):
    ordering = ['id']
    pass
