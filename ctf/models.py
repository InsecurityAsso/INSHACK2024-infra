from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class team(models.Model):
    name = models.CharField(verbose_name='Nom', max_length=50, null=False)
    password = models.CharField(verbose_name='Mot de passe', max_length=200, null=False)
    score = models.IntegerField(verbose_name='Score', null=False, default=0)
    icon_url = models.CharField(verbose_name='URL icone', max_length=200, null=False)
    description = models.TextField(verbose_name='Description', null=True)

class player(AbstractUser):
    school = models.CharField(verbose_name='École', max_length=50, null=True, blank=True)
    biography = models.TextField(verbose_name='Biographie', null=True, blank=True)
    score = models.IntegerField(verbose_name='Score', null=False, default=0, blank=True)
    is_verified = models.BooleanField(verbose_name='Est vérifié', null=False, default=False)
    id_card = models.FileField(verbose_name='Carte étudiant', null=True, blank=True)
    profile_picture = models.FileField(verbose_name='Photo de profil', null=True, blank=True)
    team = models.ForeignKey(team, verbose_name='Équipe', on_delete=models.SET_NULL, null=True, blank=True)