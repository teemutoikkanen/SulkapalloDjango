from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
'''
Kun ilmon tekijä hyväksyy jonkun haasteen luodaan uus matsi. Tuloksen laittaminen POST:lla
on mahdollista heti. Kun molemmat pelaajat on laittanu tuloksen backendi kattoo että ne on
yhteneväiset ja asettaa completed=True. Jos on eriäväisyyksiä niin molemmat RESULTit poistetaan
ja completed säilyy Falsena. Matsiin jossa on completed=True ei voi postata resulttii.
result_1 & 2 näkyvä arvo on matsin voittanut pelaaja. Tarkemmat inffot saa result modelista.
'''
class Result(models.Model):
    result_round_1_player_1 = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(30),])
    result_round_1_player_2 = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(30),])
    result_round_2_player_1 = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(30),])
    result_round_2_player_2 = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(30),])
    result_round_3_player_1 = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(30),])
    result_round_3_player_2 = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(30),])
    winner = models.ForeignKey('auth.User', blank=True, null=True, related_name='wonmatch', on_delete=models.SET_NULL)
    loser = models.ForeignKey('auth.User', blank=True, null=True, related_name='lostmatch', on_delete=models.SET_NULL)

class Matsi(models.Model):
    playerone = models.ForeignKey('auth.User', related_name='matsione', null=True, on_delete=models.SET_NULL)
    playertwo = models.ForeignKey('auth.User', related_name='matsitwo', null=True, on_delete=models.SET_NULL)
    pointsone = models.IntegerField(blank=True, null=True)
    pointstwo = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=500)
    place = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    result_1 = models.ForeignKey(Result, blank=True, null=True, related_name='match1', on_delete=models.SET_NULL)
    result_2 = models.ForeignKey(Result, blank=True, null=True, related_name='match2', on_delete=models.SET_NULL)
