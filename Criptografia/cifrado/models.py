

# Create your models here.
from django.db import models
from django.utils import timezone


class CifradoRej(models.Model):
    message = models.TextField()
    