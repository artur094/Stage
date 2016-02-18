from django.db import models
import django
from gettingstarted.settings import DATE_INPUT_FORMATS

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Utente(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(default="null")
    email = models.TextField(default="null@null.it")
    birthday = models.TextField(default=django.utils.timezone.now)
