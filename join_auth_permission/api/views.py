from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAdminUser 
from join_auth_permission.api.permissions import IsOwnerOrReadOnlyIfAdmin
from join_auth_permission.api.serializers import LoginSerializer, RegistrationSerializer, ResetPasswordConfirmSerializer, ResetPasswordSerializer, UserAccountSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import status




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
                "email":validated_user.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            

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
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        

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
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
      
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
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
