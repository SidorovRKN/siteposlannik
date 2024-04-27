from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from mainapp.models import Parts, Category
from .utils import DataMixin


# Create your views here.

class IndexView(DataMixin, ListView):
    template_name = 'mainapp/index.html'
    context_object_name = 'parts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('cat_slug')
        return self.get_mixin_context(context, default_descr="Описание товара № ХХХХ", cat_selected=cat_slug)

    def get_queryset(self):
        cat_slug = self.kwargs.get('cat_slug')
        query_string = self.request.GET.get('q')
        parts = self.get_mixin_queryset(cat_slug=cat_slug, query_string=query_string)
        return parts


class ShowPartView(DataMixin, DetailView):
    model = Parts
    template_name = 'mainapp/part.html'
    context_object_name = 'part'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    extra_context = {
        "phone": "80-177-76-36-02",
        "email": "poslannikauto@gmail.com",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part_slug = self.kwargs.get('slug')
        part = Parts.objects.get(slug=part_slug)
        return self.get_mixin_context(context, title=part.name, part=part, default_descr=f"Описание товара № {part.pk}")


class AboutView(DataMixin, TemplateView):
    template_name = "mainapp/about.html"
    title_page = 'О нас'
    extra_context = {
        'cats': Category.objects.all(),
        'num': '76-36-02',
        'email': 'some_email@gmail.com',
    }


def page_not_found(request, exception):
    return redirect(IndexView.as_view)


def servererror(request):
    return redirect('home')
