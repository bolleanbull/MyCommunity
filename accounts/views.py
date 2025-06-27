from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from django.views import generic
from django.views import View
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from .signals import account_created_email




from .forms import (
    UserLoginForm, CreateUserForm, PasswordChangeForm, PasswordResetForm
)

class  UserloginView(View):

    form = UserLoginForm()
    def get(self, request, *args, **kwargs):
        
        context = {
            'form': self.form, 
        }
        return render(request, 'accounts/login.html', context )
    
    def post(self, request, *args, **kwargs):

        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']

            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')
        else:
            messages.error(request, "Please enter the correct credentials ")

        return render(request, 'accounts/login.html', {"form": form})
        



class CreateNewUserView(View):

    def get(self,request, *args, **kwargs):

        form = CreateUserForm()
        context = {
            'form': form,

        }
        return render(request, 'accounts/create_account.html', context )
    
    def post(self, request, *args, **kwargs):

        form = CreateUserForm(request.POST)
        if form.is_valid():

            cd  = form.cleaned_data
            password = cd['password']
            username = cd['username']
            email = cd['email']

            user  = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('dashboard:index')
        else: 
            messages.error(request, "Please enter the right credentails ")
            
        return render(request, 'accounts/create_account.html', {"form": form})
    
class PasswordChangeView(View):
    
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm()

        return render(request, 'accounts/password_change.html', {"form": form})
    
    def post(self, request, *args, **kwargs):

        form = PasswordChangeForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            new_password = cd['new_password']

            user = authenticate(request,username=username, password=password)
            if user is not None:
                
                user.set_password(new_password)
                user.save()
                login(request,user)
                messages.success(request, 'Password change successfuly ')
                return redirect('dashboard:index')
            else:
                # if the user is none 
                messages.error(request, "Please enter the right credentials ")
        
        return render(request, 'accounts/password_change.html', {"form": form})
    
            



class PasswordResetView(generic.TemplateView):
    template_name = 'accounts/reset.html'
    

class PasswordResetEmailView(View):

    def post(self, request):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            reset_link = request.build_absolute_uri(
                reverse('accounts:reset_password', kwargs={'uid': user.id})
            )

            subject = "Reset Your Password"
            from_email = "admin@yourdomain.com"
            to_email = [user.email]

            context = {
                'username': user.username,
                'reset_link': reset_link
            }

            html_content = render_to_string('accounts/password_reset_email.html', context)
            text_content = f"Hi {user.username}, click the link to reset your password: {reset_link}"

            email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

        return render(request, 'accounts/email_confirmation.html')
    


class ResetPasswordView(View):

    def get(self, request, uid):
        form = PasswordResetForm()
        return render(request, 'accounts/reset_password_form.html', {'form': form})

    def post(self, request, uid):
        user = get_object_or_404(User, pk=uid)
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('accounts:login')

        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/reset_password_form.html', {'form': form})
