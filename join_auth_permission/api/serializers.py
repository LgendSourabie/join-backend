from django.contrib.auth.models import User
from rest_framework import serializers


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['id','username','email','password','confirm_password']
        extra_kwargs = {
            "password":{
                "write_only":True
            }
        }

        def save(self):
            pwd = self.validated_data['password']
            confirm_pwd = self.validated_data['confirm_password']


            if pwd != confirm_pwd:
                raise serializers.ValidationError("Passwords don't match.")
            else:
                user = User(username=self.validated_data['username'],email=self.validated_data['email'])
                user.set_password(pwd)
                user.save()
                return user

