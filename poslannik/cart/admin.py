from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order
from users.models import CustomUser


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'display_items','confirmed', 'delivered', 'usernames', 'phone',)
    list_filter = ('user', 'created_at')
    list_display_links = ('user', 'id')
    list_editable = ('confirmed', 'delivered')

    def display_items(self, obj):
        parts = "\n".join([str(part) + ' x' + str(part.quantity) for part in obj.items.all()])
        return mark_safe(format_html("<pre>{}</pre>", parts))

    display_items.short_description = 'Items'

    def usernames(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        else:
            return f"{obj.guest_name} {obj.guest_lastname}"

    def phone(self, obj):
        if obj.user:
            return f"{obj.user.phone_number}"
        else:
            return obj.guest_phone

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        print(request.user)
        # queryset = Order.objects.get(user=CustomUser.objects.get(username='admin')).items.all()
        return queryset
