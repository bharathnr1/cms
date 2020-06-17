from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.



class SignupCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    # is_active = False

    def __str__(self):
        return str(self.user)


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        print("Creating Inactive User")
        instance.is_active = False
    else:
        print("Updating User Record")