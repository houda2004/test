from django import forms
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from custom_user.models import *
from .models import *
from .utils import *

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    
#-----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})) 
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}), label="Confirm Password")
    #code = forms.CharField(max_length=10, label="Code", required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter the code'}))
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    class Meta:
        model = Person
        fields = [ 'gender', 'birthday', 'nationality','password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)  # Appelle le constructeur de la classe parente
        self.fields['email'].widget = forms.EmailInput(attrs={'type': 'email','placeholder': 'Enter the email'})  # Type email pour le champ 'email'
        self.fields['first_name'].widget = forms.TextInput(attrs={'type': 'text','placeholder': 'Enter your first name'})  # Type text pour 'first_name'
        self.fields['last_name'].widget = forms.TextInput(attrs={'type': 'text','placeholder': 'Enter your last name'})  # Type text pour 'last_name'
        self.fields['birthday'].widget = forms.DateInput(attrs={'type': 'date'})
        #if 'sign_up' in kwargs.get('data', {}):  # Check if 'sign_up' button was clicked
          #self.fields['code'].required = True  # Make code required if 'Sign Up' is clicked
        
        self.order_fields(['first_name', 'last_name', 'email', 'password', 'confirm_password', 'gender', 'birthday', 'nationality'])#, 'code'
    
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        #code = cleaned_data.get("code")
        email = cleaned_data.get("email")
        # Check if passwords match
        if password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")

        # Check if the code entered by the user matches the generated code
        '''if 'Continue' in self.data:
           #verification = EmailVerification.objects.filter(email=self.cleaned_data.get("email")).first()
           verification = EmailVerification.objects.filter(email=email).order_by('-created_at').first()
           if verification and verification.is_expired():
              raise forms.ValidationError("The verification code has expired. Please request a new one.")

           if verification and verification.code != code:
              raise forms.ValidationError(f'Invalid verification code. Please check your email.')

        return cleaned_data'''

    
    def clean_email(self):
        email = self.cleaned_data.get('email') 
        if User.objects.filter(email=email).exists(): 
            raise forms.ValidationError("This email address is already in use.") 
        return email
    
    def send_code(self, to_email):
        """Send verification code to the user's email."""
        verification = EmailVerification.objects.create(email=to_email)
        verification.save()
         # Stocker le token dans la session pour validation ultérieure
        #request.session['verification_token'] = verification.token
        return send_email(to_email,'RegistrationVerification',"Personnale/template_activate_account.html",verification.code)

        '''send_mail(
            'Your Registration Code',
            f'Your registration code is: {verification.code}',
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )'''
    def save(self, commit=True):
        # First, create the User object
        user = User(
            #username=self.cleaned_data['email'],  # Using email as the username
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=make_password(self.cleaned_data['password'])  # Hashing the password
        )

        if commit:
            user.save()  # Save the user first

        # Then, create the associated Person object
        person = super().save(commit=False)
        person.user_compte = user  # Link the user to the Person model
        if commit:
          person.save()  # Sauvegarde l'objet Person

        return person

'''def clean(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get("password") 
        confirm_password = cleaned_data.get("confirm_password") 
        if password != confirm_password: 
            raise forms.ValidationError("The passwords do not match") 
        return cleaned_data
    '''



#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

class ForgotPasswordForm(forms.Form):
    
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'type': 'email','placeholder': 'Enter your email', 'class': 'form-control'}),
        required=True
    )
    
    # Champ pour entrer le code de vérification (apparaîtra uniquement après l'envoi de l'email)
    code = forms.CharField(
        label="Code",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the verification code', 'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)  # Appelle le constructeur de la classe parente
        if 'Continue' in kwargs.get('data', {}):  # Check if 'sign_up' button was clicked
          self.fields['code'].required = True  # Make code required if 'Sign Up' is clicked
        
        self.order_fields([ 'email','code'])
    
    def clean(self):
      cleaned_data = super().clean()
      code = cleaned_data.get("code")
      email = cleaned_data.get("email")
       
      if 'Continue' in self.data:
        # Check if the code entered by the user matches the generated code
        verification = EmailVerification.objects.filter(email=email).order_by('-created_at').first()
        if verification and verification.is_expired():
            raise forms.ValidationError("The verification code has expired. Please request a new one.")

        if verification and verification.code != code:
            raise forms.ValidationError(f"Invalid verification code. Please check your email.{code} {verification}  {verification.code }")

        return cleaned_data


    def send_code(self, to_email):
        """Send verification code to the user's email."""
        verification = EmailVerification.objects.create(email=to_email)
        verification.save()
        return send_email(to_email,'ForgotPassword',"Personnale/template_activate_account.html",verification.code)


#----------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------







