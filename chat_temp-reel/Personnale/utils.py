
from django.core.mail import EmailMessage
from PROJECT.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
def send_email(to_email,subject,direction,code):#request,user,
   # Generate a random string of 6 characters, including both letters and numbers
   #token= '123456'#get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') # ajouer un token
   
   '''mail_subject = "Activate your account."
   message = render_to_string("template_activate_account.html", {
        #'user': user.username,
        #'domain': get_current_site(request).domain,
        #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #'token': account_activation_token.make_token(user),
        #"protocol": 'https' if request.is_secure() else 'http'
        'email_user':to_email,
        'code':code,
    })'''
   #email = EmailMessage(mail_subject, message, to=[to_email])# EmailMessage est utilisée pour envoyer un e-mail. Par défaut, Django utilisera l'adresse e-mail configurée dans le fichier settings.py ,qui sera utilisée est celle définie dans la variable EMAIL_HOST_USER
   #verification = EmailVerification(email=to_email, code=token)
   #verification.save()


   mail_subject = "Your password reset verification code"
   #message = f"Your verification code is: {code}\n\nUse this code to reset your password."
   message_html = render_to_string(
         direction,  #"Personnale/template_activate_account.html" Chemin vers le fichier template
        {'email_user': to_email, 'code': code,'subject':subject}  # Données à injecter dans le template
    )
   
   #send_mail(mail_subject, message, 'noreply@example.com', [to_email])
   email = EmailMessage(mail_subject, message_html, EMAIL_HOST_USER ,[to_email])  #to=            
   # Ajouter le contenu HTML à l'email
   email.content_subtype = "html"   # Indique que le contenu est en HTML
   #email.html_message = message_html  # Ajouter le contenu HTML
   
   if email.send():#code
        #messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                #received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
        return {'success': f'Dear <b>user</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.',
                'code':code
                }
   else:
        return {'error':f'Problem sending email to {to_email}, check if you typed it correctly.'}

        #messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
