from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form,
        }
        return render(request, 'users/register.html', context)
    
    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('login')
        else:
            context = {
            "form": create_form,
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'users/login.html', {"login_form": login_form})
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, "You have succesfully logged in.")
            
            return redirect("main")
        else:
            return render(request, "users/login.html", {"login_form": login_form})
        

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have succesfully logged out.")
        return redirect("login")