#from __future__ import unicode_literals
from django.db import models

# Create your models here.
class News(models.Model):
    title=models.TextField()
    link=models.TextField()
