from django.db import models
from autoslug import AutoSlugField

from src.apps.product.utils import transliterate


# Create your models here.


class Color(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    # def get_slug_value(instance):
    #     if instance.is_main:
    #         return transliterate(f'{instance.name}'.lower())
    #     return transliterate(f'{instance.parent.name}-{instance.name}'.lower())
    #
    # def get_slugify_value(value):
    #     return value.replace(' ', '-')


    def __str__(self):
        return f'{self.name}'

def get_slug_value(instance):
    if instance.is_main:
        return transliterate(f"{instance.name}".lower())
    return transliterate(f"{instance.parent.name}-{instance.name}".lower())

def get_slugify_value(value):
    return value.replace(' ','-')
class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = AutoSlugField(populate_from=get_slug_value,
                         unique=True,
                         slugify=get_slugify_value)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='sub_categories', blank=True)
    is_main = models.BooleanField('главная', default=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    title = models.CharField('Название', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('Активный', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.title}'

    @property
    def main_image(self):
        images = self.images.all()
        if images:
            return images[0].image.url
        return ''

    def get_other_images(self):
        images = self.images.all()
        if images.count() > 1:
            return images[1:]
        return []


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images/')

    def __str__(self):
        return f'{self.product}'


