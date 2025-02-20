from django_use_email_as_username.models import BaseUser, BaseUserManager

from django.db import models


class User(BaseUser):   
    objects = BaseUserManager()
   
class Person(models.Model):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ]
    NATIONALITY_CHOICES = [
    ('US', 'United States'),
    ('FR', 'France'),
    ('DZ', 'Algeria'),
    ('GB', 'United Kingdom'),
    # Add more countries as needed
    ]
    user_compte=models.OneToOneField(User,default=0,null=True, blank=True ,on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  
    #date_joined = models.DateTimeField()#auto_now_add=True
    nationality = models.CharField(max_length=2, choices=NATIONALITY_CHOICES, blank=True, null=True)
