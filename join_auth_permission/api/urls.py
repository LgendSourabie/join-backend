from django.urls import path
from . import views


urlpatterns = [
    path('users/',views.UserList.as_view(), name='users'),
    path('users/<int:pk>/',views.UserDetail.as_view(), name='user-detail'),
    path('register/',views.Registration.as_view(), name='registration'),
    path('login/',views.Login.as_view() , name='login'),
    path('password-reset-request/',views.ResetPasswordView.as_view() , name='password-reset-request'),
    path('password-reset-confirm/',views.ResetPasswordConfirmView.as_view() , name='password-reset-confirm'),
]
