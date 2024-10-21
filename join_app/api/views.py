

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from join_app.api.permissions import IsAuthenticatedOrNot
from join_app.api.serializers import  ContactSerializer, SubtaskSerializer, TaskSerializer
from rest_framework import mixins, generics
from join_app.models import Subtask, Task, Contact
from rest_framework.permissions import IsAuthenticated

class ContactList(APIView):
    """
    List all users or create a new user if data is provided
    """
    permission_classes=[IsAuthenticatedOrNot]
    
    def get(self,request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ContactDetail(APIView):
    """
    List single user , delete user, update user data
    """
    permission_classes=[IsAuthenticatedOrNot]
    
    def get_contact_or_404(self,pk):
        try: 
             contact = Contact.objects.get(pk=pk)
             return contact
        except:
            raise Http404
    
    def get(self, request, pk):
        contact = self.get_contact_or_404(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        contact = self.get_contact_or_404(pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, pk):
        contact = self.get_contact_or_404(pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserContactList(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        author = self.kwargs['author']
        return Contact.objects.filter(author=author)


class SubtaskList(mixins.ListModelMixin,mixins.CreateModelMixin,\
                  generics.GenericAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class SubtaskDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,\
                    mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
   
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class UserSubtasksList(generics.ListAPIView):
    serializer_class=SubtaskSerializer

    def get_queryset(self):
        author = self.kwargs['author']
        return Subtask.objects.filter(author=author)

    
# class CategoryList(mixins.ListModelMixin,mixins.CreateModelMixin,\
#                   generics.GenericAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
    

# class CategoryDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,\
#                     mixins.DestroyModelMixin, generics.GenericAPIView):

#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
   
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    
# class UserCategoriesList(generics.ListAPIView):
#     serializer_class=CategorySerializer

#     def get_queryset(self):
#         author = self.kwargs['author']
#         return Category.objects.filter(author=author)


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes=[IsAuthenticated]

    # def get_serializer_context(self):
    #     return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserTasksList(generics.ListAPIView):
    serializer_class=TaskSerializer

    def get_queryset(self):
        author = self.kwargs['author']
        return Task.objects.filter(author=author)