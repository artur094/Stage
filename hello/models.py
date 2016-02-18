from django.db import models
import django
from gettingstarted.settings import DATE_INPUT_FORMATS

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class User(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(default="null")
    gender = models.TextField(default="null")
    email = models.TextField(default="null@null.it")
    birthday = models.TextField(default=django.utils.timezone.now)

class Photos(models.Model):
    id = models.TextField(primary_key=True)
    date = models.TextField(default=django.utils.timezone.now)
    message = models.TextField(default="null")
