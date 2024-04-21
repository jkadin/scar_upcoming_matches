import datetime
from django.db import models
from django.utils import timezone


class Url(models.Model):
    url = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.url


class Match(models.Model):
    player1_name = models.CharField(max_length=100)
    player2_name = models.CharField(max_length=100)
    match_time = models.DateTimeField()
    tournemant_name = models.CharField(max_length=100)
