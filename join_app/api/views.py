

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from join_app.api.permissions import IsAuthenticatedOrNot, IsUserAccount
from join_app.api.serializers import  AccountsSerializer, CategorySerializer, ContactSerializer, SubtaskSerializer, TaskSerializer
from rest_framework import mixins, generics
from join_app.models import Category, Subtask, Task, Contact
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

class ContactList(APIView):
    """
    List all users or create a new user if data is provided

    This view also lists all contacts of the current authenticated. The user must 
    therefore be authenticated to see his contacts.
    """
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
 
        if (request.user.is_superuser):
            contacts = Contact.objects.all()
        else:
            contacts = Contact.objects.filter(author = request.user)
        
        serializer = ContactSerializer(contacts, many=True,context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ContactSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ContactDetail(APIView):
    """
    List single user , delete user, update user data
    
    """
    permission_classes=[IsAuthenticated & IsAuthenticatedOrNot]
    
    def get_contact_or_404(self,pk):
        try: 
             contact = Contact.objects.get(pk=pk)
             return contact
        except Contact.DoesNotExist:
            raise Http404
        
    def check_object_permission(self, request, contact):
        if not IsAuthenticatedOrNot().has_object_permission(request, self, contact):
            raise PermissionDenied("You do not have permission to access this contact.")
    
    def get(self, request, pk):
        contact = self.get_contact_or_404(pk)
        self.check_object_permission(request, contact)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        contact = self.get_contact_or_404(pk)
        self.check_object_permission(request, contact)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, pk):
        contact = self.get_contact_or_404(pk)
        self.check_object_permission(request, contact)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
class CategoryList(generics.ListAPIView):
    """
    List of all categories. Categories are not meant to be created by users.
    Super user can add or remove them. Their are available for all users and they all see 
    the same category lists.
    
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Single category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsAuthenticatedOrNot]

class SubtaskList(generics.ListAPIView):
    """Subtask list. Subtasks are created with task and are bound to the corresponding
    task. However, the list of subtask can be inspected by admin user in the backend.
    User can only see their subtasks included in their Tasks.
    """
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes=[IsAuthenticated]


    def get_queryset(self):

        pk_author=self.kwargs.get("author",None)

        if pk_author and self.request.user.is_superuser:
            return  Subtask.objects.filter(pk=int(pk_author))
        elif pk_author and self.request.user.is_authenticated:
            return  Subtask.objects.filter(author=self.request.user,pk=int(pk_author))
        elif self.request.user.is_superuser:
            return Subtask.objects.all()
        return Subtask.objects.filter(author=self.request.user.id)
    
class SubtaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Single subtask.
    """

    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes=[IsAuthenticatedOrNot]
    
class TaskList(generics.ListCreateAPIView):
    """
    This view lists all tasks of a specific user. Only the administrator can see the tasks
    of any user.
    """
    serializer_class = TaskSerializer
    permission_classes=[IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(author=self.request.user)
    

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes=[IsAuthenticatedOrNot]

    def get_serializer_context(self):
        return {'request': self.request}

class UserTasksList(generics.ListAPIView):
    """
    This view lists all tasks of the current authenticated. The user must therefore be authenticated 
    to see his tasks.
    """
    serializer_class=TaskSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(author=self.request.user)



class AccountsView(generics.ListAPIView):

    """List of user accounts if they are authenticated"""

    serializer_class = AccountsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        pk=self.kwargs.get("pk",None)

        if pk and self.request.user.is_superuser:
            return  User.objects.filter(pk=pk)
        elif(pk and self.request.user.id==int(pk)):
            return  User.objects.filter(pk=pk)
        elif self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.id)
    


    def list(self, request, *args, **kwargs):
        """enable users to see only their account
        
        Keyword arguments:
        argument -- pk : primary key oder ID of current user
        Return: list of user accounts if the user provides its id in the request
        otherwise the list all user accounts if the user is super user. If the id 
        is not the Id of the current user and the current user is not super user then 
        an un-authorization error is thrown.
        """
        
        pk=self.kwargs.get("pk",None)

        if pk and not (self.request.user.is_superuser or self.request.user.id == int(pk)):
            return Response({"error":"You don't have any permission to see this content."},
            status=status.HTTP_401_UNAUTHORIZED
            )
        return super().list(request, *args, **kwargs)

class AccountsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Single user account if the user is owner the the account or 
    is super user
    """

    serializer_class = AccountsSerializer
    permission_classes = [IsAuthenticated & IsUserAccount]

    def get_queryset(self):

        pk=self.kwargs.get("pk",None)
        return User.objects.filter(pk=int(pk))

    def get_serializer_context(self):
        return {'request': self.request}