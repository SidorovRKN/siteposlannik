from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404

from mainapp.models import Category, Parts

menu = [
    {"title": "Главная", "url_name": "home"},
    {"title": "О нас", "url_name": "about"},
    {"title": "Корзина", "url_name": "cart:view_cart"},
    {"title": "Заказы", "url_name": "cart:orders"}
    # {"title": "Контакты", "url_name": "contact"},
    # {"title": "Войти", "url_name": "users:login"},
    # {"title": "Выйти", "url_name": "users:logout"},
]


class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context: dict, **kwargs):
        context["cats"] = Category.objects.all()
        context["title"] = "Автозапчасти в Борисове"
        context.update(kwargs)
        return context

    def get_mixin_queryset(self, **kwargs):
        cat_slug = kwargs.get('cat_slug')
        query_string = kwargs.get('query_string')

        if cat_slug:
            category = get_object_or_404(Category, slug=cat_slug)
            return Parts.objects.filter(category=category, availability=True).order_by('name')
        elif query_string:
            return Parts.objects.annotate(search=SearchVector('name', 'article', 'category')).filter(
                search=query_string, availability=True)
        else:
            return Parts.objects.filter(availability=True).order_by('name')