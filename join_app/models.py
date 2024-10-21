from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name} {self.email}"

class Subtask(models.Model):
    description = models.TextField(max_length=300)
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.description}"
    

# class Category(models.Model):
#     title = models.TextField(max_length=200)
#     author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return f"{self.title}"


class Task(models.Model):
    priority_options = [('urgent','urgent'),('medium','medium'),('low','low')]
    category_option = [('technical task','technical task'), ('user story','user story'), ('others','others')]
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    due_date = models.DateField()  
    priority = models.CharField(max_length=50, choices=priority_options,default="others")
    category = models.CharField(max_length=50, choices=priority_options,default="medium")
    contacts = models.ManyToManyField(Contact, related_name='tasks')
    subtasks = models.ManyToManyField(Subtask, related_name='tasks')
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=1)


    def __str__(self):
        return f"{self.title} {self.category} {self.priority}"



# user1 = User.objects.create(username="Ibrahim Soura", email_address="sou@gmail.com",password="123456")
# user2 = User.objects.create(username="Youssef Benkahyi", email_address="soura@gmail.com",password="1234")
# user1.save()
# user2.save()
# co1 = Contact(contact_name="Moussa Soura",email_address="mssa@yahoo.bf",phone_number="1545555562",users=user1)
# co2 = Contact(contact_name="Issa Toure",email_address="Issa@yahoo.bf",phone_number="1545555562",users=user1)
# user2.save()
# co1 = Contact(contact_name="Moussa Soura",email_address="mssa@yahoo.bf",phone_number="1545555562",users=user1)
# co2 = Contact(contact_name="Issa Toure",email_address="Issa@yahoo.bf",phone_number="1545555562",users=user1)
# co1 = Contact(contact_name="Moussa Soura",email_address="mssa@yahoo.bf",phone_number="1545555562",users=user1)
# co2 = Contact(contact_name="Issa Toure",email_address="Issa@yahoo.bf",phone_number="1545555562",users=user1)
# co2 = Contact(contact_name="Issa Toure",email_address="Issa@yahoo.bf",phone_number="1545555562",users=user1)
# co3 = Contact(contact_name="Ali Traore",email_address="toura@gmx.bf",phone_number="1545555582",users=user2)
# co3 = Contact(contact_name="Ali Traore",email_address="toura@gmx.bf",phone_number="1545555582",users=user2)
# co1.save()
# co2.save()
# co1.save()
# co2.save()
# co2.save()
# co3.save()
# su1 = Subtask(description="Frontend with angular")
# su2 = Subtask(description="Frontend with React")
# su3 = Subtask(description="Meeting for user story")
# su4 = Subtask(description="Backend Interview")
# su5 = Subtask(description="Authentication with Firebase")
# su1.save()
# su2.save()
# su3.save()
# su4.save()
# su5.save()
# from datetime import datetime