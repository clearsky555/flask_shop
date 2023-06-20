from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from django.views.generic import FormView, CreateView, TemplateView
from django.http import HttpResponse

# Create your views here.

from src.apps.accounts.forms import LoginForm


class LoginView(FormView):
    template_name="login.html"
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("index")
            else:
                HttpResponse("Ваш аккаунт не активен")
        HttpResponse("Такого пользователя не существует или данные неверны")



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")