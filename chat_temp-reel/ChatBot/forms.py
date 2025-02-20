'''from django import forms
from .models import *
from Personnale.models import *'''
'''class QuestionnaireForm(forms.Form):
    # Exemple de symptômes spécifiques à chaque condition
    symptoms_choices = [
        ('sadness', 'Tristesse persistante'),
        ('loss_of_interest', 'Perte d intérêt'),
        ('fatigue', 'Fatigue excessive'),
        ('sleep_issues', 'Troubles du sommeil'),
        ('anxiety', 'Anxiété excessive'),
        ('obsessive_thoughts', 'Pensées obsessionnelles'),
        # Ajouter d'autres symptômes au besoin
    ]

    # Crée un champ pour chaque symptôme
    symptoms = forms.MultipleChoiceField(choices=symptoms_choices, widget=forms.CheckboxSelectMultiple, label="Quels symptômes ressentez-vous ?")

'''

'''
class QuestionnaireForm(forms.Form):
    # Récupérer tous les symptômes disponibles dans la base de données
    symptoms_choices = [(symptom.id, symptom.name) for symptom in Symptom.objects.all()]

    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Quels symptômes ressentez-vous ?"
    )'''