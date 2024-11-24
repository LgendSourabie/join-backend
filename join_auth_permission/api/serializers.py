from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate
from join_app.models import Contact
from join_app.api.utils import generateContactColor
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes


class UserAccountSerializer(serializers.ModelSerializer):
    """
    User account model serializer with first name and last name 
    added for enabling their view
    """
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']

class LoginSerializer(serializers.Serializer):
    """
    User login serializer to enable secure form sent. Users can login
    with email and password.
    """

    username = serializers.CharField(required = False)
    email = serializers.EmailField(required = False)
    password = serializers.CharField(write_only = True)
    remember_me = serializers.BooleanField(default=False)


    def validate(self, data):
   
        email = data.get("email",'')
        user_name = data.get('username', '')
        password = data["password"]

        if email:
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError({"error_type":"no_user_error","error_message":"No user found with this email."})
        elif user_name:
            username = user_name
        else:
            raise serializers.ValidationError({"error_type":"email_username_error","error_message":"Please provide an email or a username, field is missing."})
        
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"error_type":"incorrect_email_pwd_error","error_message":"Incorrect email or password. Please try again."})
        elif not user.is_active:
            raise serializers.ValidationError({"error_type":"disabled_account_error","error_message":"User account is disabled"})
        
        data['user'] = user
        return data

class RegistrationSerializer(serializers.ModelSerializer):
    """"
    User registration serializer allowing user to enter either the username
    and last name or not. The first name is required and when no username is 
    provided the email is set as username.
    When a user register a new contact is created with is name and he has to 
    edit his telephone after he/she logs in.
    """
    username = serializers.CharField(required = False)
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = False, allow_blank=True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username',"first_name","last_name",'email','password','confirm_password']
        extra_kwargs = {
            "password":{
                "write_only":True
            }
         
        }


    def validate(self, data):
        
        has_pwd_match = data["password"] == data["confirm_password"]
        entered_email = data['email']
        email_list = User.objects.filter(email=entered_email)

        if len(entered_email)==0:
            raise serializers.ValidationError({"error_type":"email_required","error_message":"Email address is required"})
       
        if len(email_list) > 0:
            raise serializers.ValidationError({"error_type":"email_exist","error_message":"This Email already exists. Please chose a different email."})

        if  not has_pwd_match:
             raise serializers.ValidationError({"error_type":"password","error_message":"Your passwords don't match. Try again."})
        return data

    
    def save(self):

        self.validated_data.pop('confirm_password')
        first_name = self.validated_data.pop('first_name', '')
        last_name = self.validated_data.pop('last_name', '')
        user_name = self.validated_data.pop('username','')

        if not user_name:
            user_name = self.validated_data['email']

        user = User(
            username=user_name,
            email=self.validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(self.validated_data['password'])
        user.save()
        Contact.objects.create(name=f"{last_name} {first_name}",email=self.validated_data['email'],color_pattern=generateContactColor(),telephone='XXX XXX XXX XXX',author=user)
        return user
    


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email exists.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:4200/account/reset-password/{uid}/{token}/"

        
        send_mail(
            subject="Join Password Reset",
            message=f"""
            # Hello!
            # I received your request to reset your password, which you can do by clicking below.

            # Please don't forward this email to other people, as it contains confidential information specific
            # to your account.

            # If you did not make this request then simply ignore this email.

            # Link: {reset_link}

  <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Hello {user.first_name}!</h2>
            <p>
                I received your request to reset your password. Click the button below to reset it:
            </p>
            <a href="{reset_link}" style="
                display: inline-block;
                background-color: #007BFF;
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
""",

            from_email="sourabrahim@gmail.com",
            recipient_list=[email],
        )




class ResetPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):

        has_pwd_match = data["new_password"] == data["confirm_new_password"]

        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError("Invalid user ID or token.")

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")
        
        if  not has_pwd_match:
             raise serializers.ValidationError({"error_message":"Your passwords don't match. Try again."})
        
        data['user'] = user
        return data
       

    def save(self):
   
        self.validated_data.pop('confirm_new_password')
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()