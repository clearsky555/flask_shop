from django.db import models
from src.apps.accounts.models import User
from src.apps.product.models import Product
from enum import Enum


# Create your models here.
class Order(models.Model):

    STATUS_NEW = "new"
    STATUS_REJECTED = "rejected"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DELIVERED = "delivered"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = (
        (STATUS_NEW, "Новый"),
        (STATUS_REJECTED, "Отменен"),
        (STATUS_CONFIRMED, "Подтвержден"),
        (STATUS_DELIVERED, "Доставлен"),
        (STATUS_ARCHIVED, "Архивирован")
    )


    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
                             )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_user_order = models.BooleanField("Заказ от пользователя", default=False)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default=STATUS_NEW)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"#{self.id}_{self.address}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказов"