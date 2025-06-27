

from django.urls import path
from . import views 
app_name = 'accounts'
urlpatterns  = [

    path('login/', views.UserloginView.as_view(), name='login'), 
    path('create-user/', views.CreateNewUserView.as_view(),name='create_account'), 
    path('change-password/', views.PasswordChangeView.as_view(),name='password_change'), 
    path('reset-password/', views.PasswordResetView.as_view(), name='password-reset'),
    path('reset-password-email/', views.PasswordResetEmailView.as_view(), name='password_reset_email'),
    path('reset-password/<int:uid>/', views.ResetPasswordView.as_view(), name='reset_password'),



]

