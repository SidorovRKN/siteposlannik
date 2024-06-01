from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.utils.text import slugify


def transliterate(ru_str):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V',
        'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', '-': '_',
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
        '8': '8', '9': '9', '0': '0',
    }

    # Транслитерация строки
    result = ''.join([translit_dict.get(char, char) for char in ru_str.lower() if char not in '/)(*&^"%$#+!@<>.,'])

    # Замена пробелов и других пробельных символов на подчеркивания
    result = result.replace(' ', '_')

    return result


class Category(models.Model):
    name = models.CharField(verbose_name='Наименование категории', max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = transliterate(str(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Parts(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=200, db_index=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, verbose_name='Категория')
    descr = models.TextField(verbose_name='Описание', null=True)
    slug = models.SlugField(max_length=255, null=True, unique=True)
    article = models.CharField(max_length=100, null=True)
    availability = models.BooleanField(verbose_name='Наличие', default=False)
    photo = models.ImageField(verbose_name='Фото', null=True, help_text='Загрузите изображение товара',
                              upload_to="mainapp/images")
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        slug = transliterate(str(self.name))
        if len(Parts.objects.filter(slug=slug)) > 0:
            return
        else:
            self.slug = slug
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('part', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
