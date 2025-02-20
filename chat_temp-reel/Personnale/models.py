from django.db import models

# Create your models here.
SYMPTOM_CHOICES = [
    ('sadness', 'Tristesse persistante'),
    ('loss_of_interest', 'Perte d’intérêt'),
    ('fatigue', 'Fatigue excessive'),
    ('sleep_issues', 'Troubles du sommeil'),
    ('anxiety', 'Anxiété excessive'),
    ('obsessive_thoughts', 'Pensées obsessionnelles'),
    # Vous pouvez ajouter d'autres symptômes ici si nécessaire
]
class Symptom(models.Model):
    name = models.CharField(max_length=255)  # Nom du symptôme
    #code = models.CharField(max_length=50, choices=SYMPTOM_CHOICES, unique=True)
    def __str__(self):
        return self.name

# Modèle pour stocker les maladies
class Ill(models.Model):
    name = models.CharField(max_length=100)  # Nom de la maladie
    description = models.TextField()  # Description de la maladie
    symptoms = models.ManyToManyField(Symptom, related_name="illnesse_symptoms")  # Symptômes associés à la maladie

    def __str__(self):
        return f'{self.name}: {self.description}'
    def get_symptoms_count(self):
        """Retourne le nombre de symptômes associés à la maladie."""
        return self.symptoms.count()



from django.db import models
from django.utils import timezone
from datetime import timedelta

'''class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=10)  # Code valide pendant 10 minutes
        return timezone.now() > expiration_time
''' 
import uuid  
from django.db import models
from django.utils import timezone
import random
import string

class EmailVerification(models.Model):
    email = models.EmailField(unique=False)#True
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # To set an expiration time for the code (e.g., 15 minutes)
    token = models.CharField(max_length=36, default=uuid.uuid4)#, unique=True
    def generate_code(self, length=6):
        """Generates a random alphanumeric verification code."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def is_expired(self):
        """Check if the verification code has expired."""
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        # Generate a random code before saving
        if not self.code:
            self.code = self.generate_code()#import logging '123456'
        # Si expires_at n'est pas défini, on lui attribue une expiration de 15 minutes après la création
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30) 
        super().save(*args, **kwargs)  # Appel de la méthode save parente pour enregistrer l'objet
  
'''
class Ill (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.TextField()  # Liste des symptômes associés à cette maladie

    def __str__(self):
        return f'name {self.name} description {self.description}'

'''















