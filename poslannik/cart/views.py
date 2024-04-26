from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import ListView
from mainapp.models import Parts
from mainapp.utils import DataMixin
from cart.models import Order
from cart.forms import GuestOrderForm

from users.models import CustomUser


# Create your views here.
def add_to_cart(request, product_id):
    product = Parts.objects.get(pk=product_id)

    # Проверяем, существует ли список в сессии, если нет, инициализируем его
    if 'cart' not in request.session:
        request.session['cart'] = []

    # Добавляем товар в корзину
    request.session['cart'].append(product.name)
    request.session.modified = True
    return redirect('home')


def flush_cart(request):
    if 'cart' in request.session:
        request.session['cart'] = []
    return redirect('cart:view_cart')


def remove_from_cart(request, product_id):
    product = Parts.objects.get(pk=product_id)

    if 'cart' not in request.session:
        request.session['cart'] = []

    else:
        request.session['cart'].remove(product.name)
        request.session.modified = True
    return redirect('cart:view_cart')


class CartView(DataMixin, ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'parts'
    paginate_by = 20
    title_page = "Выбранные товары"
    login_url = '/users/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('cat_slug')
        return self.get_mixin_context(context, default_descr="Описание товара № ХХХХ", cat_selected=cat_slug,
                                      title=self.title_page)

    def get_queryset(self):
        cart_product_names = self.request.session.get('cart', [])
        parts = Parts.objects.filter(name__in=cart_product_names)
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
        orders = Order.objects.filter(user=self.request.user)
        return orders


def create_order(request):
    user = request.user
    cart_items = Parts.objects.filter(name__in=request.session.get('cart', []))
    if user.is_anonymous:
        if request.method == 'POST':
            form = GuestOrderForm(request.POST)
            if form.is_valid():
                order = Order.objects.create(guest_name=form.cleaned_data['first_name'],
                                             guest_lastname=form.cleaned_data['last_name'],
                                             guest_phone=form.cleaned_data['phone'])
                order.items.set(cart_items)
                return redirect('cart:flush_cart')
        else:
            form = GuestOrderForm()
        return render(request, 'cart/guest_order_form.html', {'form': form})
    else:
        order = Order.objects.create(user=user)
        order.items.set(cart_items)
        return redirect('cart:flush_cart')
