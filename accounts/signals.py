
from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import User


account_created_email = Signal()

print('singnals ')

@receiver(post_save,sender=User)
def user_model_save(sender, instance, created, **kwargs):

    if created:
        print("The model is just created ")
    else:
        print('the model is created previously ')





