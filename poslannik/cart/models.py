from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser  # Импорт модели пользователя из приложения users
from mainapp.models import Parts  # Импорт вашей модели с товарами

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Parts, verbose_name='Заказанные запчасти')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(verbose_name='Подтвержден', default=False)
    delivered = models.BooleanField(verbose_name='Доставлен', default=False)
    guest_name = models.CharField(verbose_name='Имя', null=True, max_length=255)
    guest_lastname = models.CharField(verbose_name='Фамилия', null=True, max_length=255)
    guest_phone = models.CharField(verbose_name='Номер телефона', null=True, max_length=255)

    def __str__(self):
        return f"Order for {self.user.username}"
