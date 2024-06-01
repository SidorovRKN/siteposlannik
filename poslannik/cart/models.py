from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser  # Импорт модели пользователя из приложения users
from mainapp.models import Parts  # Импорт вашей модели с товарами
import poslannik.settings as settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Parts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(verbose_name='Подтвержден', default=False)
    delivered = models.BooleanField(verbose_name='Доставлен', default=False)
    guest_name = models.CharField(verbose_name='Имя', null=True, default='guest', max_length=255)
    guest_lastname = models.CharField(verbose_name='Фамилия', null=True, default='guest', max_length=255)
    guest_phone = models.CharField(verbose_name='Номер телефона', null=True, default='0000', max_length=255)

    def __str__(self):
        if self.user:
            return f"Order for {self.user.username}"
        else:
            return f"Order for guest"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Parts, related_name='order_item', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}'
