from src.apps.product.models import Category


def get_category(request):
    categories = Category.objects.filter(is_main=True)
    return {'categories':categories}