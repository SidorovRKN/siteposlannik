from django import forms


class GuestOrderForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    phone = forms.CharField(max_length=13, label='Телефон')
