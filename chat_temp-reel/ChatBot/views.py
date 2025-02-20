from django.shortcuts import render

# Create your views here.

from django.db.models import Count,Q, Max, OuterRef, Subquery

from django.shortcuts import render
from .forms import QuestionnaireForm
from .models import *
from Personnale.models import *
'''
def find_matching_illness(form_data):
    """
    Fonction pour trouver une maladie correspondante en fonction des symptômes fournis
    par l'utilisateur dans le formulaire.
    """
    # On récupère toutes les maladies dans la base de données
    illnesses = Ill.objects.all()
    
    # On prépare une liste des symptômes répondus par l'utilisateur
    user_symptoms = set()
    if form_data['anxiety'] == 'True':
        user_symptoms.add('anxiété')
    if form_data['stress'] == 'True':
        user_symptoms.add('stress')
    if form_data['mood_swings'] == 'True':
        user_symptoms.add('saute d\'humeur')
    if form_data['relationship_issues'] == 'True':
        user_symptoms.add('problèmes relationnels')

    # Liste pour stocker les maladies qui correspondent aux symptômes de l'utilisateur
    matching_illnesses = []

    for illness in illnesses:
        # On vérifie si tous les symptômes de l'utilisateur correspondent à cette maladie
        illness_symptoms = set(illness.symptoms.split(', '))  # On suppose que les symptômes sont séparés par des virgules
        if user_symptoms.issubset(illness_symptoms):
            matching_illnesses.append(illness)

    return matching_illnesses

def questionnaire_view(request):
    if request.method == "POST":
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # Enregistrer les réponses dans la base de données (facultatif)
            response = QuestionnaireResponse(
                anxiety=form.cleaned_data['anxiety'],
                stress=form.cleaned_data['stress'],
                mood_swings=form.cleaned_data['mood_swings'],
                relationship_issues=form.cleaned_data['relationship_issues'],
            )
            response.save()

            # Trouver les maladies correspondantes aux symptômes
            matching_illnesses = find_matching_illness(form.cleaned_data)

            if matching_illnesses:
                result = [f"{ill.name}: {ill.description}" for ill in matching_illnesses]
            else:
                result = ["Aucune maladie correspondante trouvée."]

            return render(request, 'questionnaire/result.html', {'result': result})
    else:
        form = QuestionnaireForm()

    return render(request, 'questionnaire/questionnaire.html', {'form': form})

'''

from django.shortcuts import render
from .forms import QuestionnaireForm
from .models import Ill, QuestionnaireResponse

'''def find_matching_conditions(user_symptoms):
    """
    Trouver les conditions correspondant aux symptômes de l'utilisateur.
    """
    matching_conditions = []
    illnesses = Ill.objects.all()

    for illness in illnesses:
        illness_symptoms = set(illness.symptoms.split(', '))
        if set(user_symptoms).issubset(illness_symptoms):
            matching_conditions.append(illness)

    return matching_conditions

def questionnaire_view(request):
    if request.method == "POST":
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # Récupérer les symptômes sélectionnés par l'utilisateur
            user_symptoms = form.cleaned_data['symptoms']
            
            # Enregistrer les réponses de l'utilisateur dans la base de données (facultatif)
            response = QuestionnaireResponse(symptoms=user_symptoms)
            response.save()

            # Trouver les conditions correspondant aux symptômes
            matching_conditions = find_matching_conditions(user_symptoms)

            if matching_conditions:
                result = [f"{ill.name}: {ill.description} " for ill in matching_conditions]
            else:
                result = ["Aucune condition ne correspond aux symptômes fournis."]

            return render(request, 'ChatBot/result.html', {'result': result})
    else:
        form = QuestionnaireForm()

    return render(request, 'ChatBot/questionnaire.html', {'form': form})#

'''
def choose_symptoms(request):
    #illness = Ill.objects.get(id=illness_id)  # Obtenir la maladie par son ID
    #illness= Ill.objects.all()
    symptoms = Symptom.objects.all()  # Récupérer tous les symptômes associés à cette maladie

    if request.method == "POST":
        selected_symptoms = request.POST.getlist('symptoms')  # Récupérer les symptômes sélectionnés par l'utilisateur
        # Convertir les IDs des symptômes en objets Symptom
        selected_symptoms_objects = Symptom.objects.filter(id__in=selected_symptoms)
        
        # Rechercher toutes les maladies associées aux symptômes sélectionnés
        illnesses_with_selected_symptoms = Ill.objects.filter(symptoms__in=selected_symptoms_objects).distinct()
        # Annoter chaque maladie avec le nombre de symptômes qu'elle partage avec les symptômes sélectionnés
        # Sous-requête pour compter tous les symptômes de la maladie
        # 1. Sous-requête pour obtenir le nombre total de symptômes associés à chaque maladie (via ManyToMany)
        total_symptoms_subquery = Symptom.objects.filter(
                    illnesse_symptoms=OuterRef('pk')  # Lier la sous-requête à l'ID de chaque maladie (OuterRef fait référence à l'ID de 'Ill' dans la requête principale)
           ).values('illnesse_symptoms').annotate(
               total_count=Count('id')  # Comptabiliser les symptômes distincts associés à chaque maladie
           ).values('total_count')
 
        illnesses_with_counts = illnesses_with_selected_symptoms.annotate(
            num_total_symptoms= Subquery(total_symptoms_subquery) , # Nombre total de symptômes via sous-requête
            num_matching_symptoms= Count('symptoms', filter=models.Q(symptoms__in=selected_symptoms_objects),distinct=True)
        )
       
        '''most_matching_illness = None
        max_matching_symptoms = 0
        # Passer en revue les maladies et trouver celle avec le plus grand nombre de symptômes
        for illness in illnesses_with_counts:
            if illness.num_matching_symptoms > max_matching_symptoms:
                most_matching_illness = illness
                max_matching_symptoms = illness.num_matching_symptoms
        '''
        # Trouver le maximum de num_matching_symptoms
        max_matching_symptoms = illnesses_with_counts.aggregate(
            max_symptoms=Max('num_matching_symptoms')
        )['max_symptoms']

       
        
        test_matching_illnesses= illnesses_with_counts.filter(
           num_total_symptoms=max_matching_symptoms,
           num_matching_symptoms=max_matching_symptoms
        )
        
        if test_matching_illnesses:
           most_matching_illnesses = test_matching_illnesses
        else:
           # Filtrer les maladies qui ont ce maximum
           most_matching_illnesses = illnesses_with_counts.filter(
                num_matching_symptoms=max_matching_symptoms
           ) 


        # Passer les résultats à la template pour affichage
        '''result = []
        for illness in illnesses_with_counts:
            result.append({
                'name': illness.name,
                'description': illness.description,
                'num_matching_symptoms': illness.num_matching_symptoms,
            })
            #if illness.num_matching_symptoms > max_matching_symptoms:
            #    most_matching_illness = illness
            #    max_matching_symptoms = illness.num_matching_symptoms
        '''

        if most_matching_illnesses:
          symptoms_illnesses=[]
          if most_matching_illnesses.count() > 1:     
            for illness in most_matching_illnesses:
               # Symptômes déjà sélectionnés par l'utilisateur
                  selected_symptom_ids = selected_symptoms_objects.values_list('id', flat=True)

               # Symptômes non sélectionnés pour cette maladie
                  unselected_symptoms = illness.symptoms.exclude(id__in=selected_symptom_ids)
                  if unselected_symptoms:
                     symptoms_illnesses.append({
                        'unselected_symptoms': unselected_symptoms#[symptom.name for symptom in unselected_symptoms]
                     })
            #raise ValueError(f'{symptoms_illnesses}')
            result = {
                'illnesses': most_matching_illnesses,
                'max_matching_symptoms': max_matching_symptoms,
                'symptoms_illnesses':symptoms_illnesses
            }


            '''result = []
            for illness in most_matching_illnesses:
               result.append({
                      'name': illness.name,
                      'description': illness.description,
                       'num_matching_symptoms': illness.num_matching_symptoms,
                       # Vous pouvez aussi inclure l'ID si nécessaire
                       'id': illness.id,
            }) 
            '''
            '''result = {
                'name': most_matching_illnesses.name,
                'description': most_matching_illnesses.description,
                'num_matching_symptoms': most_matching_illnesses.num_matching_symptoms,
                #'id': most_matching_illnesses.id
            }
            '''
          else:
            ill_resule=Ill.objects.get(id=most_matching_illnesses.first().id)
         # Sauvegarder les choix dans la base de données
            person=Person.objects.get(user_compte=request.user)
            user_choice = UserSymptomChoice.objects.create(user=person,resulta_final=ill_resule)  # Créer un enregistrement pour l'utilisateur
            user_choice.symptoms.set(selected_symptoms_objects)  # Associer les symptômes choisis à cet enregistrement
        
            user_choice.save()
            result = {
                'illnesses': most_matching_illnesses,
                'max_matching_symptoms': max_matching_symptoms,
                'symptoms_illnesses':''
            }
        else:
            result = None  # Aucune maladie ne correspond aux symptômes    
        
        #raise ValueError(f'{result}')
        # Traitez ici les symptômes sélectionnés, par exemple les enregistrer ou les analyser
        return render(request, 'ChatBot/result.html', { 'result':result, 'illnesses_with_selected_symptoms': illnesses_with_selected_symptoms})

    return render(request, 'ChatBot/choose_symptoms.html', {'symptoms': symptoms})#'illness': illness, 











