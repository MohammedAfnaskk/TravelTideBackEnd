from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from decouple import config

def send_activation_email(user):
    current_site = Site.objects.get_current()
    backendurl = config('backendUrl')
    current_site.domain = backendurl
    current_site.save()

    mail_subject = 'Please activate your account'
    message = render_to_string('user/email_notification.html', {
        'user': user,
        'domain': config('backendUrl'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    print('--->>>,',message)

    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
