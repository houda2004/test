from django.db import models
from custom_user.models import Person
# Create your models here.

      

class Room(models.Model):
    user1=models.ForeignKey(Person,on_delete=models.CASCADE,null=True,related_name='rooms_as_user1')
    user2=models.ForeignKey(Person,on_delete=models.CASCADE,null=True,related_name='rooms_as_user2')
    
    class Meta:
        unique_together = ('user1', 'user2')  # Assurer une seule salle par paire d'utilisateurs
        #ordering = ['user1', 'user2']  # Optional: Keep rooms ordered by users

    def __str__(self):
        return f"Room between {self.user1} and {self.user2}"
    def get_autre_user_room(self, user_sender):
        """Retourne l'autre utilisateur dans la room."""
        if self.user1 == user_sender:
            return self.user2
        elif self.user2 == user_sender:
            return self.user1
        return None  # Si l'utilisateur n'est ni user1 ni user2
    '''@staticmethod
    def get_or_create_room(user1, user2):
        # A method to return or create a room for two users, regardless of their order
        room, created = Room.objects.get_or_create(
            user1=user1,
            user2=user2,
        )
        if not created:
            return room
        
        # Ensure only one pair, user1 and user2 can have one room
        Room.objects.get_or_create(
            user1=user2,
            user2=user1,
        )
        return room'''



class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # To track if the message was read
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')  # Relation avec Room
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"   


class VideoCall(models.Model):
    caller = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='calls_made')
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='calls_received')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='video_calls')  # Relation avec la salle de discussion
    start_time = models.DateTimeField(auto_now_add=True)  # Heure de début de l'appel
    end_time = models.DateTimeField(null=True, blank=True)  # Heure de fin de l'appel (sera remplie quand l'appel est terminé)
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('ended', 'Ended')], default='in_progress')

    def __str__(self):
        return f"Video call from {self.caller} to {self.receiver} at {self.start_time}"

    def end_call(self):
        self.end_time = models.DateTimeField(auto_now_add=True)  # Enregistre l'heure de fin
        self.status = 'ended'  # Modifie le statut de l'appel
        self.save()






class Notification(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='notifications')  # L'utilisateur qui reçoit la notification
    message = models.CharField(max_length=255)  # Message de notification
    timestamp = models.DateTimeField(auto_now_add=True)  # Heure de création de la notification
    read = models.BooleanField(default=False)  # Indique si la notification a été lue
    related_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE, related_name='notifications')  # La Room liée à la notification
    #related_message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.CASCADE, related_name='notifications')  # Le message lié à la notification (facultatif)

    def __str__(self):
        return f"Notification for {self.user} at {self.timestamp} - {'Read' if self.read else 'Unread'}"