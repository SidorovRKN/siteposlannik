from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from cart import views


urlpatterns = [
    path('', views.CartView.as_view(), name='view_cart'),
    path('addcart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('removepart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('flushcart/', views.flush_cart, name='flush_cart'),
    path('order/', views.create_order, name='order'),
    path('orders/', views.OrdersView.as_view(), name='orders'),

]