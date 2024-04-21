from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order
from users.models import CustomUser


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'display_items', 'usernames', 'phone', 'guest_name', 'guest_phone')
    list_filter = ('user', 'created_at')
    list_display_links = ('user', 'id')
    readonly_fields = ['items']

    def display_items(self, obj):
        parts = "\n".join([str(part) for part in obj.items.all()])
        return mark_safe(format_html("<pre>{}</pre>", parts))

    display_items.short_description = 'Items'

    def usernames(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def phone(self, obj):
        return f"{obj.user.phone_number}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        print(request.user)
        # queryset = Order.objects.get(user=CustomUser.objects.get(username='admin')).items.all()
        return queryset
