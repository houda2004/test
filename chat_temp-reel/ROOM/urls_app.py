from django.urls import path
from ROOM import views
app_name = 'ROOM' 
urlpatterns = [
    path('', views.Contactes_user , name="Contactes_user"),
    path('<int:room_id>/', views.Contactes_user, name="Contactes_user_with_room"),
    #path('video-call/<int:id_room>/', views.fait_call_video , name="fait_call_video"),
    
    path('fait_call_video/<int:id_room>/', views.fait_call_video , name="fait_call_video"), 
    path('video-call/<int:video_call_id>/', views.video_call_page, name='video_call_page'),
    path('aller_a_call_active/<int:video_call_id>/',views.aller_a_call_active, name='aller_a_call_active'),
    path('end_call/<int:video_call_id>/',views.end_call,name='end_call'),
    #path('', views.index, name='index'),
]