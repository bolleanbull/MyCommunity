from django.db import models
from django.contrib.auth.models import User 

# Create your models here.


class Profile(models.Model):

    class GenderChoice(models.TextChoices):
        M = 'M',"Male"
        F = 'F', "Female"

    user = models.OneToOneField(User,on_delete=models.CASCADE,  related_name='profile',)
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2, choices=GenderChoice)
    address  = models.CharField(max_length=20)

    def __str__(self):
        return f'profile {self.name}'
    

    


