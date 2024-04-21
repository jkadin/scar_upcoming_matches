import datetime
from django.db import models
from django.utils import timezone

class Urls(models.Model):
    url=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.url