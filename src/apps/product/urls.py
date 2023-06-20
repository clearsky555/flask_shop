from django.urls import path

from rest_framework.routers import DefaultRouter

from src.apps.product import views

router = DefaultRouter()

router.register('product', views.ProductViewSet, basename='product')
router.register('category', views.CategoryViewSet, basename='category')


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/list/', views.ProductListView.as_view(), name='product_list'),

    path('product/add/favorite/<int:pk>', views.add_to_favorite, name='add_favorite'),
    path('product/favorites/detail/', views.favorites_detail, name='favorites_detail'),

    path('product/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:category_slug>/', views.ProductListView.as_view(), name='category_products'),
    path('product/<slug:category_slug>/<slug:subcategory_slug>/', views.ProductListView.as_view(), name='sub_products'),

]


urlpatterns += router.urls