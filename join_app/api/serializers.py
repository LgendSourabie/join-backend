from rest_framework import serializers
from join_app.models import Subtask, Contact,Task
from django.utils import timezone



class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id','name','email','phone_number']

    def create(self, validated_data):
        return super().create(validated_data)


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields=['id','description']

    def create(self, validated_data):
        return super().create(validated_data)


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields=['id','title']

#     def create(self, validated_data):
#         return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    subtasks =serializers.ListField(child=serializers.IntegerField(),write_only=True)
    contacts=serializers.ListField(child=serializers.IntegerField(),write_only=True)

    class Meta:
        model= Task
        fields=['id','title','description','due_date','priority','category','subtasks','contacts']
        
    # def __init__(self, *args, **kwargs):
    #     user = kwargs['context']['request'].user  # Get the current user
    #     super(TaskSerializer, self).__init__(*args, **kwargs)       
    #     if user.is_authenticated:
    #         self.fields['category'].queryset = Category.objects.filter(author= user)

  
    def validate_contacts(self,value):
        contacts = Contact.objects.filter(id__in=value)
        if(len(contacts) != len(value)):
            raise serializers.ValidationError('One Id not found')
        return value
    
    def validate_subtasks(self,value):
        subtasks = Subtask.objects.filter(id__in=value)
        if(len(subtasks) != len(value)):
            raise serializers.ValidationError('One Id not found')
        return value

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past or the present date.")
        return value
    


# class UserProfileSerializer(serializers.ModelSerializer):
#     contacts = ContactSerializer(many=True, read_only=True)
#     tasks = TaskSerializer(many=True, read_only=True)


#     class Meta:
#         model = UserProfile
#         fields=['id','username','email','password','contacts','tasks']
#         extra_kwargs={
#             "password":{
#                 "write_only":True
#             }
#         }


#     def create(self, validated_data):
#         validated_data['password']=make_password(validated_data['password'])
#         return User.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         if 'password' in validated_data:
#             validated_data['password']=make_password(validated_data['password'])
#         super(UserProfileSerializer, self).update(instance, validated_data)


    # def get_board_tasks(self,obj):
    #     return obj.tasks.count()
    

    # def get_number_contacts(self,obj):
    #     return obj.contacts.count()

   

    # {
    #     "id": 1,
    #     "username": "Ibrahim Traore",
    #     "email": "ibra@gmail.com"
    # },
    # {
    #     "id": 2,
    #     "username": "Youssef Benki",
    #     "email": "youssef@yahoo.com"
    # },
    # {
    #     "id": 3,
    #     "username": "Rafael Müller",
    #     "email": "mueller@yahoo.com"
    # },
    # {
    #     "id": 4,
    #     "username": "Thomas Erdinger",
    #     "email": "thomas@gmx.de"
    # }



    # 

#     [
#     {
#         "id": 1,
#         "contact_name": "Patrick Semmler",
#         "email": "patrick@gmx.de",
#         "phone_number": "015 14589871",
#         "users": 2
#     },
#     {
#         "id": 2,
#         "contact_name": "Lompo Toure",
#         "email": "lompo@gmail.bf",
#         "phone_number": "015 563558996",
#         "users": 3
#     },
#     {
#         "id": 3,
#         "contact_name": "Sylvain Vy",
#         "email": "vy@gmail.ci",
#         "phone_number": "0155 563568996",
#         "users": 1
#     },
#     {
#         "id": 4,
#         "contact_name": "Issa Sylla",
#         "email": "issa@gmx.de",
#         "phone_number": "0155 56389896",
#         "users": 1
#     },
#     {
#         "id": 5,
#         "contact_name": "Moussa Dims",
#         "email": "dim@gmx.de",
#         "phone_number": "0158 56389896",
#         "users": 1
#     },
#     {
#         "id": 6,
#         "contact_name": "Reo Soso",
#         "email": "reo@gmx.de",
#         "phone_number": "0158 56539896",
#         "users": 4
#     },
#     {
#         "id": 7,
#         "contact_name": "Phylo Reoa",
#         "email": "phil@gmx.de",
#         "phone_number": "0156 56579896",
#         "users": 4
#     }
# ]