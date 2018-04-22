from django.db import models
from ilmoitukset.models import Ilmoitus

# Create your models here.
class Haaste(models.Model):
    owner = models.ForeignKey('auth.User', related_name='haaste', on_delete=models.CASCADE)
    ilmoitus = models.ForeignKey(Ilmoitus, related_name='haaste', on_delete=models.CASCADE)
    points = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=500)
    place = models.CharField(max_length=500)