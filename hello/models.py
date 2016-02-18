from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Utente(models.Model):
    id = models.TextField
    name = models.TextField
    email = models.TextField
    birthday = models.DateField
