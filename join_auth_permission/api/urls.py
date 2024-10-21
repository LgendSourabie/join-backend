from django.urls import path
from . import views


urlpatterns = [
    path('users/',views.UserList.as_view(), name='users'),
    path('users/<int:id>/',views.UserDetail.as_view(), name='user-detail'),
    path('registration/',views.Registration.as_view(), name='registration'),
    path('login/',views.Login.as_view() , name='login'),
]
