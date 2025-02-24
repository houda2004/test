from django.shortcuts import render
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from django.utils import timezone 
from django.conf import settings
# Create your views here.
from custom_user.models import User
from .forms import *
from .models import *
from .tokens import *
from ROOM.models import *
# Create your views here.
def home(request):# affiche toute les room in home 
    psersons=Person.objects.all()
    return render(request,'Personnale/home.html',{'psersons':psersons})

def creat_room(request, id_per):
    person = Person.objects.get(id=id_per)
    user =Person.objects.get(user_compte=request.user)
    room = Room.objects.create (
            #username=self.cleaned_data['email'],  # Using email as the username
            user1=user,
            user2=person,
        )
    return redirect('home')
#----------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


def logout_act(request):
   logout(request)
   return redirect('home')

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def login_act(request):# inscrire un user déjat exicete 
    page='login'   
    if request.method == 'POST':
        email = request.POST['email']
        '''if request.POST.get('code'):
          code = request.POST['code']
          #user = authenticate(request, email=email)
          user = User.objects.get(email=email)
          test=verify_email(email,code)
          if test == "success":
            login(request, user)
            return redirect('home')
          else:
              messages.error(request, test)
      else :
       ''' 
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # ajouter la fonction de virifait email et  render vers verification email en envoir le email user 
            '''test=send_email(email)
            if test == 'error':
                 messages.error(request, f'Problem sending email to {email}, check if you typed it correctly.')
            else:
                messages.success(request, f'Dear <b> user </b>, please go to you email <b>{email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
                return render(request,'Personnale/verify_token.html',{'user':email})
             '''   
            #raise ValueError(f'{user}') # afiiche le email de user 
            login(request, user)
            #return render(request,'Personnale/verify_token.html',{'user':user})
            return redirect('home')
        else:
           messages.error(request,'email or password not correct')
    form = LoginForm()
    context={
        'page':page,
        'form':form
        }
    return render(request,'Personnale/inscrire.html',context)



#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET'])
def get_message(request):
    return Response({"message": "Bonjour depuis Django!"})
#---------------------------------------------------------------------------------------
@api_view(['POST'])
def register_user(request):
    data = request.data
    form = UserRegisterForm(data)

    '''if 'send_code' in data:
        email = data.get('email')
        if email:
            # Envoyer le code de vérification
            test=form.send_code(email)
            if 'success' in test:
                  messages.success(request, test['success'])
                  #EmailVerification.objects.filter(email=to_email).delete()
                  # Stocker le token dans la session pour validation ultérieure
                  verification = EmailVerification.objects.filter(email=email).order_by('-created_at').first()
                  request.session['verification_token'] = verification.token
            else:
                    messages.error(request, test['error'])
                    return Response({'message': f'Code sent to {email}'})
        return Response({'error': 'Email is required'}, status=400)
    '''
    if 'sign_up' in data:
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response({'message': 'User registered successfully'})
        return Response({'errors': form.errors}, status=400)

    return Response({'error': 'Invalid request'}, status=400)



def register_act(request):
    page='register'
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Handle "Send Code" button
        '''if 'send_code' in request.POST:
            if form.is_valid():
                # Send the verification code to the email
                to_email = form.cleaned_data['email']
                test=form.send_code(to_email)
                if 'success' in test:
                  messages.success(request, test['success'])
                  #EmailVerification.objects.filter(email=to_email).delete()
                  # Stocker le token dans la session pour validation ultérieure
                  verification = EmailVerification.objects.filter(email=to_email).order_by('-created_at').first()
                  request.session['verification_token'] = verification.token
                else:
                    messages.error(request, test['error'])
            else:
                messages.error(request, 'Please correct the errors in the form.')
        '''
        # Handle "Sign Up" button
        if 'sign_up' in request.POST:
            if form.is_valid():
                # Process the registration and create the user
                # Assuming you have a User model to save the data
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                # Create the user and save it (you may want to use Django's User model)
                # User.objects.create(email=email, password=password)
                #last_verification = EmailVerification.objects.filter(email=email,token=request.session.get('verification_token')).first()#all().order_by('-created_at').
                #if last_verification:    
                   #if last_verification.is_expired:     
                person = form.save(commit=True)  # Sauvegarde à la fois User et Person
                      # Se connecter directement après l'enregistrement
                user = person.user_compte
                login(request, user)
                      # Optionally, you can clear the verification code after successful registration
                      #last_verification.delete()#EmailVerification.objects.filter(email=to_email).delete()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('home')  # Redirect to login page or dashboard
                   #else:
                      # messages.error(request, 'Your verification code has expired. Please request a new code.')
                #else:
                  #  messages.error(request, 'You are change the email must resende the code or retune the old email.')
              
            else:
                messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserRegisterForm()

    return render(request, 'Personnale/inscrire.html', {'page':page,'form': form})

 


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


def Forgot_Password(request):
    page = 'forgot_password'
    
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        #to_email = form.cleaned_data['email']
        # Si l'utilisateur a appuyé sur le bouton "Send Code"
        if 'send_code' in request.POST:
            if form.is_valid():
                # Récupérer l'email soumis par l'utilisateur
                to_email = form.cleaned_data['email']
                
                try:
                    # Vérifier si l'utilisateur existe avec cet e-mail
                    user = User.objects.get(email=to_email)
                    '''
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(user.pk.encode())
                    domain = get_current_site(request).domain
                    link = f"http://{domain}/reset/{uid}/{token}/"
                    message = render_to_string('password_reset_email.html', {
                        'user': user,
                        'link': link,
                    })
                    '''
                    '''mail_subject = "Your password reset verification code"
                    message = f"Your verification code is: {verification_code}\n\nUse this code to reset your password."
                    send_mail(mail_subject, message, 'noreply@example.com', [to_email])
                    
                    # Vous pouvez stocker ce code temporairement en base de données ou dans la session pour validation
                    request.session['verification_code'] = verification_code
                    request.session['email_for_verification'] = to_email  # Conserver l'email dans la session pour la validation future
                    '''
                    test=form.send_code(to_email)
                    if 'success' in test:
                        messages.success(request, test['success'])
                        #EmailVerification.objects.filter(email=to_email).delete()
                        verification = EmailVerification.objects.filter(email=to_email).order_by('-created_at').first()
                        request.session['verification_token'] = verification.token
                    else:
                        messages.error(request, test['error'])

                except User.DoesNotExist:
                    messages.error(request, "No user found with that email address.")
            else:
                messages.error(request, "Please enter a valid email address.")
        
        
        else:
            if form.is_valid():
                # Process the registration and create the user
                # Assuming you have a User model to save the data
              to_email = form.cleaned_data['email']
                # Se connecter directement après l'enregistrement
              try:
                
                user = User.objects.get(email=to_email) 
                #last_verification = EmailVerification.objects.all().order_by('-created_at').first()
                last_verification = EmailVerification.objects.filter(email=to_email,token=request.session.get('verification_token')).first()
                if last_verification:    
                   if last_verification.is_expired:
                      login(request, user)
                      # Optionally, you can clear the verification code after successful registration
                      last_verification.delete()#EmailVerification.objects.filter(email=to_email).delete()
                      messages.success(request, 'Your account has been created successfully!')
                      return redirect('home')  # Redirect to login page or dashboard
                   else:
                       messages.error(request,'Your verification code has expired. Please request a new code.')
                else:
                    messages.error(request, 'You are change the email must resende the code or retune the email.')
              
              except User.DoesNotExist:
                    messages.error(request, "No user found with that email address.")
            
            else:
                messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ForgotPasswordForm()

    return render(request, "Personnale/inscrire.html", {'form': form, 'page': page})


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


def resend_otp():
    pass


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------







































#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


'''def register_act (request):#cree un compte
    page='register'
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            #user.username =user.username.lower()
            # ajouter la fonction de virifait email et  render vers verification email en envoir le email user 
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid form')
    context={
        'page':page,
        'form':form
             }
    return render(request,'Personnale/inscrire.html',context)
'''




#---------------------------------------------------------------------------
def verify_email(email,code):
    #email = request.POST['email']
    #code = request.POST['code']
    #raise ValueError(f'{email,code}')
    #raise ValueError(f'{request}')#poste email
    #if request.method == "POST":
    #    email = request.POST.get('email')
        token=EmailVerification.objects.filter(email=email).first()
        if token:
            #messages.error(request, "Un code de vérification a déjà été envoyé à cet email.")
            #return redirect('send_verification_email')
             if token.code == code:
                 #messages.success(request, "Votre email a été vérifié avec succès.")
                 #user = authenticate(request, email=email)
                 #user.save()
                 #login(request,user)
                 verification = EmailVerification.objects.get(email=email)
                 verification.delete()
                 return "success"
                 #return redirect('home') 
             else:
                 return "Votre email a été no vérifié."
   # return render(request,'Personnale/verify_token.html')

#--------------------------------------------------------------------------------------------------
from django.conf import settings
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

def send_verification_email(request):#revoiyer un email
    if request.method == "POST":
        email = request.POST.get('email')
        if EmailVerification.objects.filter(email=email).exists():
            messages.error(request, "Un code de vérification a déjà été envoyé à cet email.")
            return redirect('send_verification_email')

        # Génération du code de confirmation
        code = get_random_string(length=6, allowed_chars='0123456789')

        # Sauvegarder le code et l'email dans la base de données
        verification = EmailVerification(email=email, code=code)
        verification.save()

        # Envoi de l'email
        send_mail(
            'Votre code de vérification',
            f'Votre code de vérification est : {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return {'success':f"Un email de vérification a été envoyé à {email}."}
        #messages.success(request, f"Un email de vérification a été envoyé à {email}.")
        #return redirect('verify_email')

    #return render(request, 'send_verification_email.html')







