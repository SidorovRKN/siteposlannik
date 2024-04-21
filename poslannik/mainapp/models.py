
from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(verbose_name='Наименование категории', max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Parts(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=200, db_index=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, db_index=True,
                                 verbose_name='Категория')
    descr = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True, db_index=True)
    public = models.BooleanField(verbose_name='Опубликовано', default=True)
    photo = models.ImageField(verbose_name='Фото', null=True, help_text='Загрузите изображение товара',
                              upload_to="mainapp/images", blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2, default=111.11)

    def get_absolute_url(self):
        return reverse('part', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
