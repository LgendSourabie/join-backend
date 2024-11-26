  

from django.template.loader import render_to_string
import random
from django.utils.crypto import get_random_string

def message_body(username, reset_link, user_email):
    """
    This function render the email body for password reset using the template.
    """
    subject = "Join Password Reset"
    context = {
        "username": username,
        "reset_link": reset_link,
    }
    # Render the template with context
    message = render_to_string("emails/password_reset.html", context)
    from_email="contact@ibrahima-sourabie.com"
    recipient_list=[user_email,'sourabrahim@gmail.com']
    return subject,message,from_email,recipient_list



def set_full_name(first_name, last_name):
    if last_name:
        return f"{last_name} {first_name}"
    else:
        return f"{first_name}"
    


def generate_guest_email():
    domains = [
        "test.com",
        "guest.com",
        "temp.com",
        "no-mail.com",
        "mock.com",
        "demo.com",
        "rnd-mail.com",
    ]

    random_domain = random.choice(domains)
    email = f"join_{get_random_string(5)}@{random_domain}" 
    return email