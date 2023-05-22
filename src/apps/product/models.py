from django.db import models

# Create your models here.


class Color(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField(max_length=70)

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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/')

    def __str__(self):
        return f'{self.product}'


