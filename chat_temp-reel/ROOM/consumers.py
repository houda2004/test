import redis
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message,Notification,VideoCall
from custom_user.models import User ,Person
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import Person, Room, Message
# Connexion à Redis
#redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
class ChatConsumer(AsyncWebsocketConsumer):
    # Dictionnaire pour stocker les utilisateurs connectés par salle
    connected_users = {}

    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # Ajouter l'utilisateur à la liste des utilisateurs connectés
        await self.add_user_to_connected_list()

    async def disconnect(self, close_code):
        # Leave room group
        #await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # Retirer l'utilisateur de la liste des utilisateurs connectés
        await self.remove_user_from_connected_list()

        # Quitter le groupe de chat
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        
        try:
            # Essayer de charger les données JSON
            text_data_json = json.loads(text_data) 
            message = text_data_json['message']
            sender = text_data_json['sender']
            #print(f"Message reçu: {message} | Expéditeur: {sender}")
            cpt=35
            # Récupérer l'utilisateur et la salle
            user_sender =await database_sync_to_async(self.get_user_by_email)(sender)
            room = await database_sync_to_async(self.get_room_by_id)(self.room)
            
            if not user_sender:
                raise ValueError(f"L'utilisateur avec l'email {sender} n'a pas été trouvé.")
            # Sauvegarder le message dans la base de données
            receiver= await database_sync_to_async(self.get_autre_user_room)(room,user_sender)
            msg = await database_sync_to_async(self.create_message)(user_sender, room, message,receiver)
            '''response={
                'message':msg.message,
                'receiver':msg.receiver,
                'timestamp':msg.timestamp
            }
            '''
            cpt=51
            #if receiver:
              #await database_sync_to_async(self.create_notification)(receiver,user_sender,room)
            
            # Vérifier si le récepteur est connecté
            is_receiver_connected = await self.is_user_connected(receiver)
            cpt=55
            if not is_receiver_connected:
                # Envoyer une notification si le récepteur n'est pas connecté
                await database_sync_to_async(self.create_notification)(receiver, user_sender, room)
            
            # Envoyer le message au groupe
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                    #'donne': json.dumps(response)
                    #'msg': {
                    #    'receiver': receiver,
                    #    'timestamp': str(msg.timestamp)
                    #}
                }
            )
            if msg:
            # Envoyer le message à un utilisateur spécifique via WebSocket
             '''await self.send(text_data=json.dumps({
                'message': msg.message,
                'sender': user_sender,
                'receiver': receiver,
                'timestamp': msg.timestamp
            }))'''
             
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Données JSON invalides reçues.'
            }))
        except ValueError as e:
            print(f"Erreur de validation des données: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
        except ObjectDoesNotExist as e:
            print(f"Objet non trouvé (utilisateur/salle): {e}")
            await self.send(text_data=json.dumps({
                'error': 'Utilisateur ou salle introuvable.'
            }))
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            await self.send(text_data=json.dumps({
                'error': f'Une erreur est survenue lors du traitement de votre message.{cpt}'
            }))

    async def chat_message(self, event):
        message = event['message']
        sender_email = event['sender']
        #msg = event['msg']
        #last_message= await database_sync_to_async(self.get_last_massege)(sender_email)
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_email,
            #'msg': msg
            #'last_message':last_message
        }))
     
    # Méthodes synchrones pour accéder aux objets de la base de données
    def get_user_by_email(self, email):
        user=User.objects.get(email=email)
        return Person.objects.get(user_compte=user) 
    
    def get_room_by_id(self, room_id):
        return Room.objects.get(id=room_id)

    def create_message(self, user_sender, room, message,receiver):
        return Message.objects.create(
            sender=user_sender,
            room=room,
            message=message,
            receiver=receiver
        )
    
    def get_autre_user_room(self,room, user_sender):
        return  room.get_autre_user_room(user_sender)
    
    def get_last_massege(self,sender):
        user=User.objects.get(email=sender)
        person=Person.objects.get(user_compte=user)
        return Message.objects.filter(sender=person).order_by('-id').first()
    
    def create_notification(self,receiver,user_sender,room):
        Notification.objects.create(
                 user=receiver,
                 message=f"New message from {user_sender.user_compte.first_name} {user_sender.user_compte.last_name}",
                 related_room=room,
                 #related_message=msg
                )
    
    async def add_user_to_connected_list(self):
        # Ajouter l'utilisateur à la liste des utilisateurs connectés
        user = self.scope['user']
        if user.is_authenticated:
            if self.room not in self.connected_users:
                self.connected_users[self.room] = set()
            self.connected_users[self.room].add(user.id)

    async def remove_user_from_connected_list(self):
        # Retirer l'utilisateur de la liste des utilisateurs connectés
        user = self.scope['user']
        if user.is_authenticated and self.room in self.connected_users:
            self.connected_users[self.room].discard(user.id)

    async def is_user_connected(self, user):
        # Vérifier si l'utilisateur est connecté
        return self.room in self.connected_users and user.id in self.connected_users[self.room]







    '''async def add_user_to_connected_list(self):
        # Ajouter l'utilisateur à la liste des utilisateurs connectés
        user = self.scope['user']
        if user.is_authenticated:
            await sync_to_async(self._add_user_to_connected_list)(user)

    def _add_user_to_connected_list(self, user):
        # Ajouter l'utilisateur à la liste Redis
        redis_client.sadd(f"connected_users_{self.room}", user.id)

    async def remove_user_from_connected_list(self):
        # Retirer l'utilisateur de la liste des utilisateurs connectés
        user = self.scope['user']
        if user.is_authenticated:
            await sync_to_async(self._remove_user_from_connected_list)(user)

    def _remove_user_from_connected_list(self, user):
        # Retirer l'utilisateur de la liste Redis
        redis_client.srem(f"connected_users_{self.room}", user.id)

    async def is_user_connected(self, user):
        # Vérifier si l'utilisateur est connecté
        return await sync_to_async(self._is_user_connected)(user)

    def _is_user_connected(self, user):
        # Vérifier si l'utilisateur est dans la liste Redis
        return redis_client.sismember(f"connected_users_{self.room}", user.id)
    '''



#from flask import Flask, render_template
#from flask_socketio import SocketIO, emit

#------------------------------------------
    '''
class CallConsumer(AsyncWebsocketConsumer):
    connected_users = {}
    async def connect(self):
        self.video_call_id = self.scope['url_route']['kwargs']['video_call_id']
        self.room_group_name = f'video_call_{self.video_call_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # Ajouter l'utilisateur à la liste des utilisateurs connectés
        await self.add_user_to_connected_list()

    async def disconnect(self, close_code):
        await self.remove_user_from_connected_list()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
      try:
        data = json.loads(text_data)
        
        message_type = data['type']
        #message_type = data.get('type')
        sender = self.scope['user']
        cpt=245
        video_call=await database_sync_to_async(self.get_video_call)(self.video_call_id)
        cpt=247
        video_call_caller=await database_sync_to_async(self.get_video_caller)(self.video_call_id)#video_call.caller
        video_call_receiver=await database_sync_to_async(self.get_video_receiver)(self.video_call_id)#video_call.receiver
        cpt=249
        person =await database_sync_to_async(self.get_user_by_email)(sender)
        # Vérifier que l'utilisateur est autorisé
        if not sender.is_authenticated:
            await self.close()
            return
        if person == video_call_caller or person == video_call_receiver:

           # Gérer les différents types de messages
          cpt=261
          if message_type == 'offer':
            #await self.handle_offer(data, sender)
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'send_offer', 'offer': data['offer']}
            )
          elif message_type == 'answer':
            #await self.handle_answer(data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'send_answer', 'answer': data['answer']}
            )
          elif message_type == 'candidate':
            #await self.handle_ice_candidate(data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'send_candidate', 'candidate': data['candidate']}
            )
          #elif message_type == 'call-end':
            #await self.handle_call_end()
          elif message_type == 'media_blocked':
              await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'send_candidate', 'media_blocked': data['media_blocked']}
            )
          else:
            await self.send_error(f"Type de message non supporté {str(message_type)}")
        else:
            await self.send_error("tu peux etre ici")
      except json.JSONDecodeError:
        await self.send_error("Format JSON invalide")
      except Exception as e:
        #logger.error(f"Erreur WebSocket: {str(e)}")
        #await self.send_error("Erreur interne du serveur")
        await self.send(text_data=json.dumps({
                'error': f'Erreur interne du serveur{cpt},,,, {str(message_type)},,,,,{str(e)}.'
            }))
    async def send_offer(self, event):
        await self.send(text_data=json.dumps({'type': 'offer', 'offer': event['offer']}))

    async def send_answer(self, event):
        await self.send(text_data=json.dumps({'type': 'answer', 'answer': event['answer']}))

    async def send_candidate(self, event):
        await self.send(text_data=json.dumps({'type': 'candidate', 'candidate': event['candidate']}))
    '''  
   #---------------------------------------------------------------------------
   
   
    '''async def handle_offer(self, data, sender):
      """Transmet l'offre SDP au destinataire"""
      await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'relay.message',
            'payload': {
                'type': 'offer',
                'offer': data['offer'],
                'sender_id': str(sender.id)
            }
        }
    )

    async def handle_answer(self, data):
      """Transmet la réponse SDP à l'appelant"""
      await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'relay.message',
            'payload': {
                'type': 'answer',
                'answer': data['answer']
            }
        }
    )

    async def handle_ice_candidate(self, data):
      """Transmet les candidats ICE"""
      await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'relay.message',
            'payload': {
                'type': 'ice-candidate',
                'candidate': data['candidate']
            }
        }
    )

    async def handle_call_end(self):
      """Notifie la fin d'appel à tous les participants"""
      await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'relay.message',
            'payload': {
                'type': 'call-end'
            }
        }
    )

    async def relay_message(self, event):
       """Transmet le message à tous sauf l'émetteur original"""
       if self.channel_name != event.get('sender_channel'):
          await self.send(text_data=json.dumps(event['payload']))
    '''
    #------------------------------------
    '''async def send_error(self, message):
      await self.send(text_data=json.dumps({
        'type': 'error',
        'message': message
    }))'''
    #--------------------------------------  


    '''  async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )
'''
    '''async def call_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
    '''
    #-------------------------------------------------------
    '''
    def get_video_call(self,id_video):
        return  VideoCall.objects.get(id=id_video)
    def get_user_by_email(self, email):
        user=User.objects.get(email=email)
        return Person.objects.get(user_compte=user) 
    def get_video_caller(self,id_video):
        return  VideoCall.objects.get(id=id_video).caller
    def get_video_receiver(self,id_video):
        return  VideoCall.objects.get(id=id_video).receiver

    async def add_user_to_connected_list(self):
      user = self.scope['user']
      if user.is_authenticated:
        if self.room_group_name not in self.connected_users:  # Corrigé
            self.connected_users[self.room_group_name] = set()
        self.connected_users[self.room_group_name].add(user.id)

    async def remove_user_from_connected_list(self):
      user = self.scope['user']
      if user.is_authenticated and self.room_group_name in self.connected_users:  # Corrigé
        self.connected_users[self.room_group_name].discard(user.id)

    async def is_user_connected(self, user):
       return self.room_group_name in self.connected_users and user.id in self.connected_users[self.room_group_name]  # Corrigé
    '''
    #-------------------------------------------------------------
    '''async def add_user_to_connected_list(self):
        # Ajouter l'utilisateur à la liste des utilisateurs connectés
        user = self.scope['user']
        if user.is_authenticated:
            if self.room not in self.connected_users:
                self.connected_users[self.room] = set()
            self.connected_users[self.room].add(user.id)

    async def remove_user_from_connected_list(self):
        # Retirer l'utilisateur de la liste des utilisateurs connectés
        user = self.scope['user']
        if user.is_authenticated and self.room in self.connected_users:
            self.connected_users[self.room].discard(user.id)

    async def is_user_connected(self, user):
        # Vérifier si l'utilisateur est connecté
        return self.room in self.connected_users and user.id in self.connected_users[self.room]
'''

'''
class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )

    async def call_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

'''


#----------------------------------------------------------------------
#-----------------------  Call Consumer  ---------------------------

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['video_call_id']
        self.room_group_name = f"call_{self.room_name}"

        # Rejoindre le groupe de la salle
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de la salle
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        # Envoyer le signal au groupe de la salle
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': message_type,
                'data': data
            }
        )

    async def offer(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def answer(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def candidate(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def message(self, event):
        # Gérer d'autres types de messages (par exemple, notifications)
        await self.send(text_data=json.dumps({
            'type': 'message',
            'content': event['content']
        }))

































'''class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
      try:
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
       
        # Retrieve the user and room from the database
        user_sender = Person.objects.get(email=sender)
        room = Room.objects.get(id=self.room)
        # Récupérer l'utilisateur et la salle depuis la base de données
        #user_sender = await database_sync_to_async(Person.objects.get)(email=sender)  # Utilisez l'email pour récupérer l'utilisateur
        #room = await database_sync_to_async(Room.objects.get)(id=self.room)
        # Save the message to the database
        msg = Message.objects.create(
            sender=user_sender,
            room=room,
            message=message
        )
         # Sauvegarder le message dans la base de données
        #await database_sync_to_async(self.create_message)(user_sender, room, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender 
            }
        )
      except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Données JSON invalides reçues.'
            }))

      except ValueError as e:
            print(f"Erreur de validation des données: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

      except Exception as e:
            print(f"Erreur inattendue: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Une erreur est survenue lors du traitement de votre message.'
            }))
            
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender':sender
        }))
'''
'''class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room}'

        # Rejoindre le groupe de la salle
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de la salle
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Sauvegarder le message dans la base de données
        user1 = Person.objects.first()  # À remplacer par l'utilisateur actuel
        user2 = Person.objects.last()   # À remplacer par l'autre utilisateur
        room = Room.get_or_create_room(user1, user2)
        message = Message.objects.create(sender=user1, receiver=user2, message=message_content, room=room)

        # Envoyer le message à tous les membres du groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    '''
'''
    async def connect(self):
        # Fetch users (this is just an example, you'd typically fetch users from authentication)
        user1 = Person.objects.first()  # Replace with actual user fetching logic
        user2 = Person.objects.last()   # Replace with actual user fetching logic

        # Get or create a room for these two users
        self.room = Room.get_or_create_room(user1, user2)
        self.room_group_name = f'chat_{self.room.id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Save the message to the database
        sender = Person.objects.first()  # Replace with actual sender logic
        receiver = Person.objects.last()  # Replace with actual receiver logic
        message = Message.objects.create(sender=sender, receiver=receiver, message=message_content, room=self.room)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    '''