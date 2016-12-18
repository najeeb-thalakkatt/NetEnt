__author__ = 'najeeb'

"""
Genre Model
"""
from django.db import models


class Genre(models.Model):

    """
    Genre model for genre table.
    """
    genre_str = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'genre'
