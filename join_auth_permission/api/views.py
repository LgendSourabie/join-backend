from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAdminUser 
from join_app.api.utils import generate_contact_color
from join_app.models import Contact
from join_auth_permission.api.permissions import IsOwnerOrReadOnlyIfAdmin
from join_auth_permission.api.serializers import LoginSerializer, RegistrationSerializer, ResetPasswordConfirmSerializer, ResetPasswordSerializer, UserAccountSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import status
import random
from join_auth_permission.api.utils import generate_guest_email, set_full_name




class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAdminUser]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes=[IsOwnerOrReadOnlyIfAdmin]

class Login(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data =request.data )
        
        if serializer.is_valid():
            validated_user =serializer.validated_data['user']
            remember_me=serializer.validated_data.get('remember_me',False)
            
            token, _ = Token.objects.get_or_create(user=validated_user)

            login(request, validated_user)

            if remember_me:
                request.session.set_expiry(2*24*60*60)
            else:
                request.session.set_expiry(0)

            data={
                "token":token.key,
                "username":validated_user.username,
                "email":validated_user.email,
                 "is_guest": False,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuestLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = generate_guest_email()
        first_name = 'Guest'

        user = User.objects.create_user(
            username=generate_guest_email() ,
            email=email,
            first_name=first_name,
        )
        user.save()
        Contact.objects.create(name=set_full_name(first_name,last_name=''),email=email,color_pattern=generate_contact_color(),telephone='XXX XXX XXX XXX',author=user)

        login(request, user)
   
        token, _ = Token.objects.get_or_create(user=user)

   
        return Response({
            "token": token.key,
            "email": user.email,
            "first_name": user.first_name,
            "is_guest": True,
        }, status=status.HTTP_200_OK)

class Registration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data =request.data )
        
        if serializer.is_valid():
            saved_account = serializer.save()
            token, _ = Token.objects.get_or_create(user=saved_account)
            data={
                "token":token.key,
                "username":saved_account.username,
                "email":saved_account.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordView(APIView):
    """
    This enable the user to send a request for resetting their 
    password when forgotten

    """
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent to your email!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class ResetPasswordConfirmView(APIView):
    """
    This enable the user to reset their 
    password when forgotten

    """
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Password successfully reset!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
