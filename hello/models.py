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

class Photo(models.Model):
    id = models.TextField(primary_key=True)
    id_owner = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    date = models.TextField(default=django.utils.timezone.now)
    message = models.TextField(default="null")

class CommentedPhoto(models.Model):
    id_photos = models.ForeignKey(Photo, on_delete=models.CASCADE, default=-1)
    id_reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    date = models.TextField(default=django.utils.timezone.now)

