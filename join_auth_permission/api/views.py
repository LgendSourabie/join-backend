from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny 
from join_auth_permission.api.serializers import RegistrationSerializer, UserAccountSerializer
from join_auth_permission.models import UserAccount



class UserList(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class Login(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data =request.data )
        
        if serializer.is_valid():
            validated_user = serializer.validated_data['user']
            token, is_created = Token.objects.get_or_create(user=validated_user)
            data={
                "token":token.key,
                "username":validated_user.username,
                "email":validated_user.email
            }
        else:
            data = serializer.errors

        return Response(data)

class Registration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data =request.data )
        
        if serializer.is_valid():
            saved_account = serializer.save()
            token, is_created = Token.objects.get_or_create(user=saved_account)
            data={
                "token":token.key,
                "username":saved_account.username,
                "email":saved_account.email
            }
        else:
            data = serializer.errors

        return Response(data)