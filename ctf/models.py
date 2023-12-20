from django.db import models

# Create your models here.

# create a player model
class player(models.Model):
    id = models.IntegerField(name='id', verbose_name='Identifiant utilisateur', primary_key=True, unique=True, auto_created=True, editable=False, null=False)
    last_name = models.CharField(name='last_name', verbose_name='Nom', max_length=50, null=False)
    first_name = models.CharField(name='first_name', verbose_name='Nom', max_length=50, null=False)
    email = models.EmailField(name='email', verbose_name='Email', max_length=75, null=False)
    school = models.CharField(name='school', verbose_name='Ecole', max_length=50, null=False)
    password = models.CharField(name='password', verbose_name='Mot de passe', max_length=200, null=False)
    student_card_filename = models.CharField(name='student_card_filename', verbose_name='Nom fichier carte étudiant', max_length=50, null=False)
    biography = models.TextField(name='biography', verbose_name='Biographie', null=True)
    



# create a team model
class team(models.Model):
    id = models.IntegerField(name='id', verbose_name='Identifiant équipe', primary_key=True, unique=True, auto_created=True, editable=False, null=False)
    name = models.CharField(name='name', verbose_name='Nom', max_length=50, null=False)
    password = models.CharField(name='password', verbose_name='Mot de passe', max_length=200, null=False)
    score = models.IntegerField(name='score', verbose_name='Score', null=False, default=0)
    icon_url = models.CharField(name='icon_url', verbose_name='URL icone', max_length=200, null=False)
