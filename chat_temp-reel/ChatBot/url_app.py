from django.urls import path
from . import views
app_name = 'ChatBot'
urlpatterns = [
    #path('',views.questionnaire_view, name='questionnaire'),#cree un compte
    path('', views.choose_symptoms, name='questionnaire'),
]