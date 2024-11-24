from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  
        subject = "Welcome To My Join App!"
        message = f"""
Dear {instance.first_name if instance.first_name else instance.username},

Welcome to Join!

Thank you for registering an account with me. I am thrilled to have you join my app user community. With Join, you can:

- Create and manage tasks effortlessly with a user-friendly interface.  
- Add and organize your contacts to collaborate effectively.  
- Assign tasks to specific contacts to ensure everyone knows their responsibilities.  
- Track the progress of your projects and stay on top of deadlines.  

If you have any questions or improvement suggestions you can reach me anytime at contact@ibrahima-sourabie.com.

I hope you enjoy using my platform to streamline your project management and boost your productivity. I look forward to supporting your success!

Best regards,  
Ibrahima SOURABIE
Join  
"""
        from_email = 'sourabrahim@gmail.com'
        recipient_list = [instance.email,'sourabrahim@gmail.com']
        send_mail(subject, message, from_email, recipient_list)