from django.urls import path
from . import views
urlpatterns = [
    #path('login/',views.LoginPage,name="login"),
    #path('logup/',views.logUpPage,name="logup"),
    
    path('', views.home , name="home"),
    path('logout/',views.logout_act, name='logout'),
    path('login/',views.login_act, name='login'),# inscrire un user déjat exicete 
    #path('register/',views.register_user, name='register'),#cree un compte 
    path('register/',views.register_act, name='register'),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path('Forgot_Password/',views.Forgot_Password,name='ForgotPassword'),
    path('message/', views.get_message, name='get_message'),
    #path('login/verify_email/',views.verify_email,name='verify_email')
]