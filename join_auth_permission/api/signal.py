from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  
        subject = "Welcome To My Join App!"
        context = {
            "first_name_or_username": instance.first_name if instance.first_name else instance.username,
        }
        message = render_to_string("emails/registration.html", context)

        from_email = 'sourabrahim@gmail.com'  
        recipient_list = [instance.email,'sourabrahim@gmail.com']
        email_to_send = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list

        ) 

        email_to_send.content_subtype = "html"
        email_to_send.send()
  



    