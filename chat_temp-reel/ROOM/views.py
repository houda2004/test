
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.utils import timezone
from datetime import timedelta
# Create your views here.



'''def Contactes_user(request,room_id=None):


    # Get the current user
    current_user = request.user  # Assuming `request.user` is the logged-in user
    person_current=Person.objects.get(user_compte=current_user)
    # Filter rooms where current_user is either user1 or user2
    rooms = Room.objects.filter(user1=person_current) | Room.objects.filter(user2=person_current)
    rooms_with_other_user = []
    for room in rooms:
        # Get the other user for the current room
        other_user = room.get_autre_user_room(person_current)
        rooms_with_other_user.append({'room': room, 'other_user': other_user})
    # Get the selected room ID from query params or URL
    #room_id = request.GET.get('room_id') or request.resolver_match.kwargs.get('room_id') 
    # Get the selected room ID from query params or URL
    #room_id = room_id or request.GET.get('room_id')
    selected_room = None
    messages = []
    videoCalls=[]
    combined_timeline = []
    selected_room_other_user=""
    if room_id:
        selected_room = Room.objects.get(id=room_id)
        messages = Message.objects.filter(room=selected_room).order_by('timestamp')
        videoCalls=VideoCall.objects.filter(room=selected_room).order_by('end_time')
        #messages.update(read=True)
        # Marquer tous les messages non lus de cette salle comme lus
        Message.objects.filter(room=selected_room, read=False).update(read=True)
        # Marquer toutes les notifications de cette salle comme lues
        Notification.objects.filter(related_room=selected_room, read=False).update(read=True)

        # Combine messages and video calls into one list with a common timestamp for sorting
        selected_room_other_user=selected_room.get_autre_user_room(person_current)
        for message in messages:
            combined_timeline.append({
                'type': 'message',  # Indicating this is a message
                'timestamp': message.timestamp,
                'sender': message.sender,
                'receiver': message.receiver,
                'content': message.message,
            })
        
        for call in videoCalls:
            combined_timeline.append({
                'type': 'video_call',  # Indicating this is a video call
                'timestamp': call.start_time,
                'caller': call.caller,
                'receiver': call.receiver,
                'start_time': call.start_time,
                'end_time': call.end_time,
                'status': call.status,
                'id':call.id
            })

        # Sort the combined timeline by timestamp
        combined_timeline = sorted(combined_timeline, key=lambda x: x['timestamp'])

    #return render(request, 'ROOM/contactes.html', {
    #    'rooms': rooms,
    #   'selected_room': selected_room,
     #   'messages': messages,
     #   'videoCalls': videoCalls
   # })
    return render(request, 'ROOM/contactes.html', {
        'rooms': rooms,
        'selected_room': selected_room,
        'selected_room_other_user': selected_room_other_user,
        'combined_timeline': combined_timeline,
        'person_current':person_current,
        'rooms_with_other_user':rooms_with_other_user
    })
'''




def Contactes_user(request,room_id=None):
    # Get the current user
    current_user = request.user  # Assuming `request.user` is the logged-in user
    person_current=Person.objects.get(user_compte=current_user)
    # Filter rooms where current_user is either user1 or user2
    rooms = Room.objects.filter(user1=person_current) | Room.objects.filter(user2=person_current)
    rooms_with_other_user = []
    '''for room in rooms:
        # Get the other user for the current room
        other_user = room.get_autre_user_room(person_current)
        rooms_with_other_user.append({'room': room, 'other_user': other_user})
   '''
    selected_room = None
    # pour react => 
    rooms_with_other_user = [
        {'id': room.id, 'other_user': room.get_autre_user_room(person_current).user_compte.first_name} for room in rooms
    ]
    
    messages = []
    videoCalls=[]
    combined_timeline = []
    selected_room_other_user=""
    if room_id:
        selected_room = Room.objects.get(id=room_id)
        messages = Message.objects.filter(room=selected_room).order_by('timestamp')
        videoCalls=VideoCall.objects.filter(room=selected_room).order_by('end_time')
        #messages.update(read=True)
        # Marquer tous les messages non lus de cette salle comme lus
        Message.objects.filter(room=selected_room,receiver=person_current ,read=False).update(read=True)
        # Marquer toutes les notifications de cette salle comme lues
        Notification.objects.filter(related_room=selected_room,user=person_current, read=False).update(read=True)

        # Combine messages and video calls into one list with a common timestamp for sorting
        
        #selected_room_other_user=selected_room.get_autre_user_room(person_current)
        
        #pour react =>
        content = ''
        selected_room_other_user=selected_room.get_autre_user_room(person_current).user_compte.first_name
        for message in messages:
            
            
            if (message.message_type == 'audio') :
                content = message.audio_data
            elif (message.message_type == 'text') :
                content = message.message
            elif (message.message_type == 'file') :
                content = message.file_url
            
                
            combined_timeline.append({
                'type': 'message',  # Indicating this is a message
                'timestamp': message.timestamp,
                #'sender': message.sender,# dans react on peux pas envoiyer des object
                #'receiver': message.receiver,# dans react on peux pas envoiyer des object 
                'sender': message.sender.user_compte.first_name,
                'receiver': message.receiver.user_compte.first_name,
                #'content':  message.message,
                'id':message.id,
                'type_msg':message.message_type,
                'content':content,
            })
        
        for call in videoCalls:
            combined_timeline.append({
                'type': 'video_call',  # Indicating this is a video call
                'timestamp': call.start_time,
                #'caller': call.caller,# dans react on peux pas envoiyer des object
                #'receiver': call.receiver,# dans react on peux pas envoiyer des object
                'caller': call.caller.user_compte.first_name,
                'receiver': call.receiver.user_compte.first_name,
                'start_time': call.start_time,
                'end_time': call.end_time,
                'status': call.status,
                'id':call.id
            })

        # Sort the combined timeline by timestamp
        combined_timeline = sorted(combined_timeline, key=lambda x: x['timestamp'])

    return JsonResponse({
        'rooms': rooms_with_other_user,
        #'rooms_with_other_user': rooms_with_other_user,
        'selected_room': selected_room.id if selected_room else None,
        'combined_timeline': combined_timeline,
        'person_current': person_current.user_compte.first_name,
        'selected_room_other_user': selected_room_other_user,
        #'rooms': rooms,
    })


from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import time
import random
import string

AGORA_APP_ID = "b4ec67d6d68743cd83cba0ee704c55ac"
AGORA_APP_CERTIFICATE = "d2a19bab9e594434a71765403e2c21ab"

def generate_token(request,id_call):
    """Génère un token Agora pour un appel vidéo"""
    current_user = request.user  # Assuming `request.user` is the logged-in user
    person_current=Person.objects.get(user_compte=current_user)
    try:
        call_session =VideoCall.objects.get(id=id_call)
    except VideoCall.DoesNotExist:
        return JsonResponse({"error": "Call not found"}, status=404)

    channel_name = str(id_call) #''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    uid =person_current.id #random.randint(1000, 9999)
    expiration_time_in_seconds = 1800
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds
    
    token = RtcTokenBuilder.buildTokenWithUid(
       AGORA_APP_ID, AGORA_APP_CERTIFICATE, channel_name, uid, 1, privilege_expired_ts
    )
    ''' - 1 (Publisher) : Cela signifie que l'utilisateur est un émetteur (publisher), c'est-à-dire qu'il peut envoyer de la vidéo et de l'audio dans la session de chat ou de conférence en temps réel.
        - 2 (Subscriber) : Cela signifie que l'utilisateur est un abonné (subscriber), c'est-à-dire qu'il peut uniquement recevoir de la vidéo et de l'audio, mais il ne peut pas en envoyer.
        - 0 (Admin) : Cela signifie que l'utilisateur a un privilège d'administrateur et peut gérer des aspects comme accorder ou révoquer des privilèges pour d'autres utilisateurs.
    '''


    #raise ValueError(f'{channel_name}...{uid}...{ privilege_expired_ts}...{token}')
    # Sauvegarder la session en base de données
    #CallSession.objects.create(channel_name=channel_name)
    
    return JsonResponse({
        'channel_name': channel_name,
        'uid': uid,
        'token': token
       #'id_user':str(person_current.id)
    })
















def fait_call_video(request,id_room):
    current_user = request.user  # Assuming `request.user` is the logged-in user
    person_current=Person.objects.get(user_compte=current_user)
    #room_id = request.POST.get(id_room)
    selected_room = Room.objects.get(id=id_room)
    selected_room_other_user=selected_room.get_autre_user_room(person_current)
    # Create the video call record
    video_call = VideoCall.objects.create(
        caller=person_current,
        receiver=selected_room_other_user,
        room=selected_room,
        status='in_progress'
    )
    context={
        'selected_room':selected_room,
        'selected_room_other_user':selected_room_other_user,
        'person_current':person_current,
        'video_call_id': video_call.id
    }
     # Return a response with the video call information
    #return redirect(f'/Contactes/video-call/{video_call.id}/') #render(request,'ROOM/vidio_call.html',context) #JsonResponse({'message': 'Video call initiated', 'video_call_id': video_call.id}, status=200)#to indicate the success of the video call initiation.
    # Redirection vers la page d'appel avec le bon paramètre
    return redirect('ROOM:video_call_page', video_call_id=video_call.id)
'''
def fait_call_video(request,id_room=None):
    current_user = request.user  # Assuming `request.user` is the logged-in user
    person_current=Person.objects.get(user_compte=current_user)
    #room_id = request.POST.get(id_room)
    if id_room:
       selected_room = Room.objects.get(id=id_room)
       selected_room_other_user=selected_room.get_autre_user_room(person_current)
    # Create the video call record
       video_call = VideoCall.objects.create(
        caller=person_current,
        receiver=selected_room_other_user,
        room=selected_room,
        status='in_progress'
      )
       context={
        'selected_room':selected_room,
        'selected_room_other_user':selected_room_other_user,
        'person_current':person_current,
        'video_call': video_call,
        #'websocket_url': f"wss://{request.get_host()}/ws/video-call/{video_call.id}/"
       }
    return render(request,'ROOM/video_call.html',context) #JsonResponse({'message':
     # Return a response with the video call information
    #return redirect(f'/Contactes/video-call/{video_call.id}/') #render(request,'ROOM/vidio_call.html',context) #JsonResponse({'message': 'Video call initiated', 'video_call_id': video_call.id}, status=200)#to indicate the success of the video call initiation.
'''
def end_call(request, video_call_id):
    if request.method == 'POST':
        video_call = get_object_or_404(VideoCall, id=video_call_id)
        video_call.status = 'completed'
        video_call.end_time = timezone.now()
        video_call.save()
        #return JsonResponse({'status': 'success'})
        return redirect(f'/Contactes/') 


def aller_a_call_active(request,video_call_id):
    return redirect(f'/Contactes/video-call/{video_call_id}/') 


def video_call_page(request,video_call_id):
    video_call = get_object_or_404(VideoCall, id=video_call_id)
    #user=User.objects.get(email=email)
    person_courant=Person.objects.get(user_compte=request.user)    #return render(request, 'ROOM/vidio_call.html', {'video_call': video_call})
    #return render(request, 'ROOM/video_call.html', {'video_call': video_call})
    #return render(request, 'ROOM/test_vid.html', {'video_call': video_call,'person_courant':person_courant})  #
    return render(request,'ROOM/video.html',{'video_call': video_call,'person_courant':person_courant})
    #return render(request,'ROOM/vid.html',{'video_call': video_call,'person_courant':person_courant})
def get_notifications(request): 
    person= Person.objects.get(user_compte= request.user )# L'utilisateur connecté
    notifications = Notification.objects.filter(user=person, read=False)  # Notifications non lues

    return render(request, 'CHAT_TEMP/navBar.html', {'notifications': notifications})


def index(request):
    return render(request, 'ROOM/chat.html')




