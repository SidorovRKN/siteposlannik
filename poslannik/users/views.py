
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterUserForm

# Create your views here.
menu = [
    {"title": "О нас", "url_name": "about"},
    {"title": "Контакты", "url_name": "contact"},
    {"title": "Войти", "url_name": "users:login"},
]

#
# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # создание объекта без сохранения в БД
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return HttpResponseRedirect(reverse('home'))
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})
#

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy('about')


class LogoutUser(LogoutView):
    next_page = 'home'


def logout_user(request):
    logout(request)
    print(request.POST)
    print(request.GET)
    return HttpResponseRedirect(reverse('home'))
