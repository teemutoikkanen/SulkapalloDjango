from django.db import models

# Create your models here.
class Ilmoitus(models.Model):
    owner = models.ForeignKey('auth.User', related_name='ilmoitus', on_delete=models.CASCADE)
    points = models.IntegerField(blank=True, null=True)
    title = models.TextField(max_length=1000)
    time = models.CharField(max_length=500)
    place = models.CharField(max_length=500)