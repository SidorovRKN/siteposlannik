from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from cart.models import Order
from users.forms import RegisterUserForm, ProfileUserForm
from users.models import CustomUser


# Create your views here.


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

    def get_success_url(self):
        user = CustomUser.objects.get(username=self.request.POST['username'])
        orphan_orders = Order.objects.filter(guest_phone=user.phone_number)
        if orphan_orders.exists():
            for order in orphan_orders:
                order.user = user
                order.save()
        print(self.request.POST)
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    next_page = 'home'


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
