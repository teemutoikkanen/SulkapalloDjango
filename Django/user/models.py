from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

# This model extends the Django's base user model by using OneToOneField as
# a link to the original user model, which contains the logging information.
# Here we define the additional fields that we need.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	points = models.IntegerField(default=1000, blank=True, editable=False)
	phone = models.CharField(max_length=20, unique=True)
	
#Any new user that gets created will also get a token associated with their account
#Note that users that were created before adding this code snippet might not have a token associated with their account
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
			
			
'''
Alla olevia ei sittenkään varmaan tarvita koska usermodelien luonti ja päivitys hoidetaan
serializerin avulla, joka luo sekä userin että profilen. Tulis muuten tupla luonti.
'''	
# #signals explained in https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# #basically make sure our custom model gets created any time we create/update User instances
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
	# if created:
		# Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
	# instance.profile.save()

