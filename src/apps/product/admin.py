from django.contrib import admin
from django import forms

# Register your models here.
from src.apps.product.models import Product, ProductImage, Category


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        prefix = "HH"
        if "мужская" in obj.parent.name:
            prefix = "Мужские"
        elif "женская" in obj.parent.name:
            prefix = "Женские"
        elif "детская" in obj.parent.name:
            prefix = "Детские"

        return f"{prefix} {obj.name}"


class CategoryAdminForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(is_main=True), required=False)

    class Meta:
        model = Category
        fields = ['name', 'parent', 'is_main']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = [
        'name',
        'slug',
        'is_main',
    ]
    list_filter = [
        'is_main',
    ]
    search_fields = [
        'name',
    ]
    # prepopulated_fields = {'slug':('name',)}


class ProductIMageInline(admin.StackedInline):
    model = ProductImage
    extra = 5


class ProductAdminForm(forms.ModelForm):
    category = CategoryChoiceField(
        queryset=Category.objects.filter(is_main=False),
        )
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductIMageInline]
    list_display = [
        'title',
        'category',
        'price',
        'is_active',
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'category',
        'price',
        'created_at',
        'is_active',
    ]
    search_fields = [
        'title',
        'description',
    ]


