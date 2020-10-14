from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Produkt(models.Model):
    id = models.IntegerField(primary_key=True)
    tip = models.CharField(max_length=50, null=True)
    emer = models.CharField(max_length=50, null=True)
    img_src = models.CharField(max_length=255, null=True)
    pershkrim = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.emer


class Dyqan(models.Model):
    id = models.IntegerField(primary_key=True)
    emer = models.CharField(max_length=50, null=True)
    adresa = models.CharField(max_length=50, null=True)
    logo = models.CharField(max_length=255, null=True)

    produkte = models.ManyToManyField(Produkt, through='DyqanProdukt')

    def __str__(self):
        return self.emer


# per te ruajtur fusha shtese (sasine dhe cmimin e produktit ne varesi te dyqanit)
class DyqanProdukt(models.Model):
    produkt = models.ForeignKey(Produkt, null=True, on_delete=models.CASCADE)
    dyqan = models.ForeignKey(Dyqan, null=True, on_delete=models.CASCADE)

    cmimi = models.FloatField(null=True)
    sasia = models.IntegerField(default=1, null=True)

    class Meta:
        unique_together = [['produkt', 'dyqan']]

    def __str__(self):
        return self.produkt.emer



    def inkremento(self):
        self.sasia = self.sasia + 1

    def dekremento(self):
        self.sasia = self.sasia - 1


class Profil(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    porosite = models.ManyToManyField(DyqanProdukt)


    def __str__(self):
        return self.user.username
