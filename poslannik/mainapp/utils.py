from django.contrib.postgres.search import SearchVector
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
        if kwargs.get('cat_slug'):
            return Parts.objects.filter(category=Category.objects.get(slug=kwargs.get('cat_slug')), availability=True).order_by('name')
        elif kwargs.get('query_string'):

            result = (Parts.objects.annotate(
                search=SearchVector('name', 'article', 'category'))
                      .filter(search=kwargs.get('query_string'), availability=True))
            return result

        else:
            return Parts.objects.filter(availability=True).order_by('name')