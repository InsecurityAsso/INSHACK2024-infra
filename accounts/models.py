from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.


class team(models.Model):
    name = models.CharField(verbose_name='Nom', max_length=50, null=False)
    password = models.CharField(verbose_name='Mot de passe', max_length=200, null=False)
    score = models.IntegerField(verbose_name='Score', null=False, default=0)
    icon = models.ImageField(verbose_name='Icone', null=True, blank=True, upload_to='team_icons/')
    description = models.TextField(verbose_name='Description', null=True)

class player(AbstractUser):
    school = models.CharField(verbose_name='École', max_length=50, null=True, blank=True)
    biography = models.TextField(verbose_name='Biographie', null=True, blank=True)
    score = models.IntegerField(verbose_name='Score', null=False, default=0, blank=True)
    is_verified = models.BooleanField(verbose_name='Est vérifié', null=False, default=False)
    id_card = models.FileField(verbose_name='Carte étudiant', null=True, blank=True, upload_to='id_docs/')
    profile_picture = models.ImageField(verbose_name='Photo de profil', null=True, blank=True, upload_to='profile_pictures/')
    team = models.ForeignKey(team, verbose_name='Équipe', on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ManyToManyField(Group, verbose_name='Groupes', blank=True) # required for admin


class token(models.Model):
    token = models.CharField(verbose_name='Token', max_length=200, null=False)
    player_email = models.CharField(verbose_name='Email joueur', max_length=200, null=False)
    action = models.CharField(verbose_name='Action', max_length=10, null=False)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True, null=False)

    # show as player_email - action - date in admin
    def __str__(self):
        return f'{self.player_email} - {self.action} - {self.date.strftime("%d/%m/%Y %H:%M:%S")}'
    
