from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Parts, Category


@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'category', 'descr', 'brief_info', 'availability', 'slug')
    list_display_links = ('slug', 'name', 'category')
    list_editable = ('descr', 'availability')
    list_per_page = 50
    actions = ['set_published', 'hide']
    list_filter = ['category__name', 'availability']
    search_fields = ['name', 'category__name']
    fields = ['name', 'photo', 'slug', 'descr', 'category', 'availability', 'price']
    # readonly_fields = ['slug']

    @admin.display(description='Кол-во символов описания', ordering='name')
    def brief_info(self, part: Parts):
        return f"Описание {len(part.descr)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(public=True)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Скрыть выбранные записи")
    def hide(self, request, queryset):
        count = queryset.update(public=False)
        self.message_user(request, f"Изменено {count} записи(ей).")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')
    list_display_links = ('name', 'pk')
    ordering = ('pk',)
