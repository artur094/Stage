from django.db import models
from django.db.models import Q
import django
from gettingstarted.settings import DATE_INPUT_FORMATS


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Coppia(models.Model):
    id = models.AutoField(primary_key=True)
    lui = models.TextField(default="")
    lei = models.TextField(default="")
    comune = models.TextField(default="")
    date = models.DateField(default=django.utils.timezone.now)

    @staticmethod
    def add_coppia(lui, lei, comune):
        if not Coppia.objects.filter(lui=lui).filter(lei=lei).filter(comune=comune).exists():
            sposi = Coppia()
            sposi.lei = lei
            sposi.lui = lui
            sposi.comune = comune
            sposi.save()
        else:
            sposi = Coppia.objects.get(Q(comune=comune), Q(lui=lui), Q(lei=lei))
        return sposi


class User(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(default="")
    gender = models.TextField(default="")
    email = models.TextField(default="")
    birthday = models.TextField(default=django.utils.timezone.now)

class Photo(models.Model):
    id = models.TextField(primary_key=True)
    id_owner = models.ForeignKey('User', on_delete=models.CASCADE, default=-1)
    created_time = models.TextField(default=django.utils.timezone.now)
    name = models.TextField(default="")

class CommentedPhoto(models.Model):
    id_photos = models.ForeignKey('Photo', on_delete=models.CASCADE, default=-1)
    id_reporter = models.ForeignKey('User', on_delete=models.CASCADE, default=-1)
    date = models.TextField(default=django.utils.timezone.now)

class Friend(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=-1, related_name='user')
    friend = models.ForeignKey('User', on_delete=models.CASCADE, default=-1, related_name='friend')

class Post(models.Model):
    id_post = models.TextField(primary_key=True)
    id_creator = models.ForeignKey(User, on_delete=models.CASCADE, default=-1, related_name='id_creator')
    date = models.TextField(default=django.utils.timezone.now)
    story = models.TextField(default="")
    description = models.TextField(default="")
    type = models.TextField(default="")
    to = models.ForeignKey(User, on_delete=models.CASCADE, default=-1, related_name='to')