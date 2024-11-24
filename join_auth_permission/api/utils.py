  

def message_body(username,reset_link,user_email):
    subject="Join Password Reset"
    message=f"""
            <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <h2>Hello {username}!</h2>
                        <p>
                            I received your request to reset your password. Click the button below to reset it:
                        </p>
                        <a href="{reset_link}" style="
                            display: inline-block;
                            background-color: #2a3647;
                            color: white;
                            text-decoration: none;
                            padding: 10px 20px;
                            border-radius: 1000px;
                            font-size: 16px;
                            font-weight: bold;
                        ">Reset Password</a>
                        <p style="margin-top: 20px;">
                            If you did not make this request, simply ignore this email.
                        </p>
                        <p>
                            Please don't forward this email to others as it contains sensitive information.
                        </p>
                        <p>Best regards,<br>Join</p>
                    </body>
                </html>
            """

    from_email="contact@ibrahima-sourabie.com"
    recipient_list=[user_email,'contact@ibrahima-sourabie.com']
    return subject,message,from_email,recipient_list


def set_full_name(first_name, last_name):
    if last_name:
        return f"{last_name} {first_name}"
    else:
        return f"{first_name}"