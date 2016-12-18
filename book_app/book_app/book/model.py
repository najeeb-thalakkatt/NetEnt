__author__ = 'najeeb'

from django.db import models

from book_app.genre.model import Genre


class Book(models.Model):
    """
    Book Model used for book table
    """
    book_title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    # As a book can have many genres
    genres = models.ManyToManyField(Genre)

    class Meta:
        managed = True
        db_table = 'book'
