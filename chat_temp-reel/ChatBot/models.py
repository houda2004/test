from django.db import models
from Personnale.models import *
# Create your models here.
from custom_user.models import *

class Question (models.Model):
    question_text = models.CharField(max_length=200)
    mal = models.ForeignKey(Ill,on_delete=models.CASCADE,name='questions_ill')


from django.db import models

class QuestionnaireResponse(models.Model):
    # Symptomes fournis par l'utilisateur (on utilise un champ TextField pour stocker une liste des symptômes)
    symptoms = models.TextField()

    # On peut ajouter d'autres informations si nécessaire, comme l'ID utilisateur si on veut l'associer à un utilisateur connecté
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Date et heure de la réponse pour un meilleur suivi
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response from {self.date_submitted} - Symptoms: {self.symptoms[:50]}...'

# we use it 
class UserSymptomChoice(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)  # L'utilisateur qui fait le choix
    symptoms = models.ManyToManyField(Symptom)  # Les symptômes choisis par l'utilisateur
    resulta_final=models.ForeignKey(Ill, on_delete=models.CASCADE)
    date_chosen = models.DateTimeField(auto_now_add=True)  # La date à laquelle l'utilisateur a fait ce choix
 
    def __str__(self):
        return f"Choix de symptômes de {self.user.user_compte.first_name} le {self.date_chosen}"





