from django.urls import path
from src.apps.cart import views


urlpatterns = [
    path('detail/', views.CartTemplateView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', views.add_cart, name='add_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),


]