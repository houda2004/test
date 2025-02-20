from django.shortcuts import get_object_or_404
from ROOM.models import Notification
from custom_user.models import Person

# pour affiche les notification dans tout les page qui avoir un navBar
def notifications(request):
    notifications = []  # Par défaut, aucune notification

    if request.user.is_authenticated:  # Vérifie si l'utilisateur est connecté
        try:
            # Récupérer l'objet Person associé à l'utilisateur connecté
            #person = get_object_or_404(Person, user_compte=request.user)
            person = Person.objects.get(user_compte=request.user)
            # Récupérer les notifications non lues pour cet utilisateur
            notifications = Notification.objects.filter(user=person, read=False)
        except Person.DoesNotExist:
              # Si l'utilisateur n'a pas de profil Person, retourner une liste vide
              notifications = []
    else:
        # Si l'utilisateur n'est pas connecté, retourner une liste vide
        notifications = []

    # Retourner un dictionnaire contenant les notifications
    return {'notifications': notifications}
