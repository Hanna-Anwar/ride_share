# Signal runs automatically when a User is saved.

from user_app.models import *

from django.db.models.signals import post_save

from django.dispatch import receiver

@receiver(post_save,sender=User)
def  create_profile(sender,instance,created,**kwargs):

    if created:

        Profile.objects.create(user=instance)