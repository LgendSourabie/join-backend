from django.urls import path
from . import views


urlpatterns = [ 
    path('accounts/',views.AccountsView.as_view(), name='accounts-list'),
    path('accounts/<int:pk>/',views.AccountsView.as_view(), name='accounts-detail'),
    path('users/accounts/<int:pk>/',views.AccountsDetail.as_view(), name='accounts-user-detail'),
    path("contacts/",views.ContactList.as_view(), name='contact-list'),
    path("contacts/<int:pk>/",views.ContactDetail.as_view(), name='contact-detail'),
    path("categories/",views.CategoryList.as_view(), name='category-list'),
    path("categories/<int:pk>/",views.CategoryDetail.as_view(), name='category-detail'),
    path("subtasks/",views.SubtaskList.as_view(), name='subtasks-list'),
    path("subtasks/<int:pk>/",views.SubtaskDetail.as_view(), name='subtasks-detail'),
    path("users/subtasks/<int:author>/",views.SubtaskList.as_view(), name='subtasks-list'),
    path("tasks/",views.TaskList.as_view(), name='task-list'),
    path("tasks/<int:pk>/",views.TaskDetail.as_view(), name='task-detail'),
]
