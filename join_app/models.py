from django.db import models
from django.contrib.auth.models import User
from join_app.api.utils import generateContactColor


class Contact(models.Model):
    
    name=models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=20,blank=True, null=True)
    color_pattern = models.CharField(max_length=25, default=generateContactColor())
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'email'],
                name='unique_contact_email_per_user'
            ),
            models.UniqueConstraint(
                fields=['author', 'telephone'],
                name='unique_contact_telephone_per_user'
            )
        ]

    def __str__(self):
        return f"{self.name} {self.email}"

class Subtask(models.Model):
    description = models.TextField(max_length=300)
    is_completed =models.BooleanField(default=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.description}"

class Category(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.title}"    
    
class Task(models.Model):
    priority_options = [('urgent','urgent'),('medium','medium'),('low','low')]
    task_group_options = [('await feedback','await feedback'),('todo','todo'),('done','done'),('in progress','in progress')]
    category_options = [('technical task','technical task'), ('user story','user story'),('team event','team event'), ('others','others')]
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    due_date = models.DateField()  
    category = models.CharField(max_length=50, choices=category_options,default="others")
    priority = models.CharField(max_length=50, choices=priority_options,default="medium")
    task_group = models.CharField(max_length=50, choices=task_group_options,default="todo")
    assigned_to = models.ManyToManyField(Contact, related_name='tasks')
    subtasks = models.ManyToManyField(Subtask,related_name='tasks')
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)


    def __str__(self):
        return f"{self.title} {self.category} {self.priority}"


