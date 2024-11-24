from rest_framework import serializers
from join_app.models import Category, Subtask, Contact,Task
from django.utils import timezone
from django.contrib.auth.models import User


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id','name','email','telephone','color_pattern']
    


    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        email = data.get('email')
        telephone = data.get('telephone')

        instance_id = self.instance.id if self.instance else None
 
        if Contact.objects.filter(author=user, email=email).exclude(id=instance_id).exists():
            raise serializers.ValidationError({
                'email': 'You already have a contact with this email.'
            })

        if telephone and Contact.objects.filter(author=user, telephone=telephone).exists():
            raise serializers.ValidationError({
                'telephone': 'You already have a contact with this telephone number.'
            })

        return data

class CategorySerializer(serializers.ModelSerializer):
    """
    category serializer which enable only the title of a category  
  
    """
    class Meta:
        model = Category
        fields = ['id','title']

class SubtaskSerializer(serializers.ModelSerializer):
    """
    subtask serializer accepting the description of the task which 
    cannot be left blank. If so then the task will be created but the 
    corresponding description will not be consider.
    
    """

    description = serializers.CharField(required=True,allow_blank=False)
    class Meta:
        model = Subtask
        fields=['id','description','is_completed']

    def create(self, validated_data):
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    """
    - Task serializer accepting subtasks and assigned contacts when
    the task is being created. Here the assigned contacts and subtasks
    fields (the others remain normal)  need to be passed as follow:
    {
    "task_subtasks":[{"description":"enter your description"}, {"description":"enter your description"},etc...]
    "assigned_to_contact_ids":[1,2,5] // list of IDs of the contacts to be assigned the task
    } 

    - When updating a task the two field must be passed on the same way but for TASK_SUBTASK the dic- field must 
    have the id of each subtask which need to be updated (added to "description") otherwise a new subtask will be created
   
    """
    

    description = serializers.CharField(required=False)
    subtasks = SubtaskSerializer(many=True, read_only = True)
    assigned_to =ContactSerializer(many=True, read_only = True)
    task_subtasks = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
    assigned_to_contact_ids =serializers.ListField(child=serializers.IntegerField(),write_only=True, required=False)
    class Meta:
        model= Task
        fields=['id','title','description','due_date','priority','category','task_group','subtasks','task_subtasks','assigned_to','assigned_to_contact_ids']

    def create(self, validated_data):
        assigned_to_contact_ids = validated_data.pop('assigned_to_contact_ids',[])
        task_subtasks_data = validated_data.pop('task_subtasks',[])

        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assigned_to_contact_ids)

        subtask_instances = []
        for subtask_data in task_subtasks_data:

            if len(subtask_data["description"]) != 0:
                subtask_instance, created = Subtask.objects.get_or_create(**subtask_data)
                subtask_instances.append(subtask_instance)
            else:
                raise serializers.ValidationError({"blank_field_error":"This field is required"})
        task.subtasks.set(subtask_instances)
        return task
    

    def update(self, instance, validated_data):
        assigned_to_contact_ids = validated_data.pop('assigned_to_contact_ids', None)
        task_subtasks_data = validated_data.pop('task_subtasks', None)

        instance = super().update(instance, validated_data)

        if assigned_to_contact_ids is not None:
            instance.assigned_to.set(assigned_to_contact_ids)

        subtask_instances = []

        if task_subtasks_data is not None:
            for subtask_data in task_subtasks_data:
                subtask_id = subtask_data.get('id')
                if subtask_id:
                    subtask_instance = Subtask.objects.get(id=subtask_id)
                    subtask_instance.description = subtask_data.get('description', subtask_instance.description)
                    subtask_instance.is_completed = subtask_data.get('is_completed', subtask_instance.is_completed)
                    subtask_instance.save()
                else:
                    subtask_instance = Subtask.objects.create(**subtask_data)
                subtask_instances.append(subtask_instance)

            instance.subtasks.set(subtask_instances)

        instance.refresh_from_db()

        return instance
    

    def validate_assigned_to_contact_ids(self,value):
        user = self.context['request'].user
        contacts = Contact.objects.filter(id__in=value)
        contact_ids = Contact.objects.filter(id__in=value).values_list('author_id', flat=True)
        contact_ids = list(contact_ids)
        if(len(contacts) != len(value)):
            raise serializers.ValidationError('One Id not found')
        elif not all(pk == user.id for pk in contact_ids):
            raise serializers.ValidationError("You cannot assign a contact that does not belong to you.")
        return value
    
    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past or the present date.")
        return value
    

class AccountsSerializer(serializers.ModelSerializer):
    """
    Account serializer enabling contacts and tasks in one user account. 
    When the user data is fetched all his contacts and tasks will be included 
    in the contacts. 
    """
    
    contacts = ContactSerializer(many = True, read_only=True, source='contact_set')
    tasks = TaskSerializer(many = True, read_only=True, source='task_set')


    class Meta:
        model =User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'contacts', 'tasks']


