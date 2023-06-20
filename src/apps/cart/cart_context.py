from src.apps.cart.cart import Cart


def get_cart_context(request):
    return {'cart': Cart(request)}