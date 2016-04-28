from django.db import models
from django.db.models import Q
import django
from gettingstarted.settings import DATE_INPUT_FORMATS


# Create your models here. :)
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
    username = models.TextField(default="")
    RSAname = models.TextField(default="")
    RSAlocation = models.TextField(default="")
    RSAmagazine = models.TextField(default="")

class Magazine(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=-1)
    edition = models.IntegerField(default=0)
    date = models.TextField(default=django.utils.timezone.now)

class Magazine_type(models.Model):
    id = models.AutoField(primary_key=True)
    magazine = models.ForeignKey('Magazine', on_delete=models.CASCADE, default=-1)
    type = models.TextField(default="")

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    magazine_type = models.ForeignKey('Magazine_type', on_delete=models.CASCADE, default=-1)
    img_src = models.TextField(default="#")
    #user creator
    id_creator = models.TextField(default='')
    #gathered ondemand, so we will have the username and profile's image up to date
    username_creator = models.TextField(default='')
    img_src_creator = models.TextField(default='')
