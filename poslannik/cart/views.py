from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from mainapp.models import Parts
from mainapp.utils import DataMixin
from cart.models import Order, Cart, CartItem, OrderItem
from cart.forms import GuestOrderForm

from users.models import CustomUser


# Create your views here.
@login_required
def add_to_cart(request, product_id):
    product = Parts.objects.get(pk=product_id)
    user = request.user
    user_cart, created = Cart.objects.get_or_create(user=user)
    user_cart_items = CartItem.objects.filter(cart__user=user, product=product)
    if user_cart_items.exists():
        item = user_cart_items.first()
        item.quantity += 1
        item.save()
    else:
        cart, created = Cart.objects.get_or_create(user=user)
        CartItem.objects.create(cart=cart, product=product)
    return redirect('home')


@login_required
def flush_cart(request):
    user = request.user

    cart_items = CartItem.objects.filter(cart__user=user)
    if cart_items:
        cart_items.delete()

    return redirect('cart:view_cart')


@login_required
def remove_from_cart(request, product_id):
    product = Parts.objects.get(pk=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    if not created:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart:view_cart')


class CartView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'parts'
    paginate_by = 20
    title_page = "Выбранные товары"
    login_url = '/users/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('cat_slug')
        user = self.request.user
        cart = CartItem.objects.filter(cart__user=user)
        return self.get_mixin_context(context, default_descr="Описание товара № ХХХХ", cat_selected=cat_slug,
                                      title=self.title_page, cart=cart)

    def get_queryset(self):
        user = self.request.user
        parts = CartItem.objects.filter(cart__user=user)

        return parts


class OrdersView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'cart/orders.html'
    context_object_name = 'orders'
    paginate_by = 20
    title_page = "Ваши заказы"
    login_url = '/users/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('cat_slug')
        return self.get_mixin_context(context, default_descr="Описание товара № ХХХХ", cat_selected=cat_slug,
                                      title=self.title_page)

    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user)
        return order


@login_required
def create_order(request):
    user = request.user
    order = Order.objects.create(user=user)
    for obj in CartItem.objects.filter(cart__user=user):
        OrderItem.objects.create(order=order, product=obj.product,
                                 price=obj.product.price, quantity=obj.quantity)

    return redirect('cart:flush_cart')
