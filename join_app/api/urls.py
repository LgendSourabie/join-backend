from django.urls import path
from . import views


urlpatterns = [ 
    path("contacts/",views.ContactList.as_view()),
    path("contacts/<int:pk>/",views.ContactDetail.as_view()),
    path("users/<int:author>/contacts/",views.UserContactList.as_view()),
    path("subtasks/",views.SubtaskList.as_view()),
    path("subtasks/<int:pk>/",views.SubtaskDetail.as_view()),
    path("users/<int:author>/subtasks/",views.UserSubtasksList.as_view()),
    path("tasks/",views.TaskList.as_view()),
    path("tasks/<int:pk>/",views.TaskDetail.as_view()),
    path("users/<int:author>/tasks/",views.UserTasksList.as_view()),
]

