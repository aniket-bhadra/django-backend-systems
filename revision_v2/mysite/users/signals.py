from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#receving signals if sender = user then fire that fn
@receiver(post_save,sender=User)
# sender- which sends the signal
# instance - instance that is being saved
# created - holds boolean value,which tell if the user created or not
def build_profile(sender,instance,created,**kwargs):
   if created:
      Profile.objects.create(user=instance)



# @receiver(post_save,sender=User)
# def save_profile(sender,instance,**kwargs):
#    instance.profile.save()