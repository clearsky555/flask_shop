from django.contrib import admin

# Register your models here.
from src.apps.order.models import Order, OrderItem


class OrderItemStackedInline(admin.StackedInline):
    model = OrderItem
    extra = 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemStackedInline]
    list_display = ["user", "address", "postal_code", "id"]