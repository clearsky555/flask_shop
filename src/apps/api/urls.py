from django.urls import path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from src.apps.api import views

router = DefaultRouter()
# router.register('user', views.UserGetViewSet, basename='user')
# router.register('user/add_favorite', views.UserAddFavorite, basename='user_add_favorite')
# router.register('user/remove_favorite', views.UserRemoveFavorite, basename='user_remove_favorite')
# router.register('favorites/<int:pk>', views.UserGetFavoriteSet, basename='user_favorites')



schema_view = get_schema_view(
    openapi.Info(
        title="FlaskShop API",
        default_version='v1',
        description="FlaskShop",
        contact=openapi.Contact(email="clearsky21555@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    path('docs/', schema_view.with_ui('swagger')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/change_password/', views.ChangePasswordAPIView.as_view()),
    path('user/register/', views.RegisterAPIView.as_view()),
    path('user/update/', views.UserUpdateAPIView.as_view()),

    #endpoints for favorites product
    path('user/add/favorite/<int:pk>/', views.AddFavoriteProduct.as_view()),
    path('user/remove/favorite/<int:pk>/', views.RemoveFavoriteProduct.as_view()),
    path('user/favorites/list/', views.UserProductFavoritesList.as_view()),
]

urlpatterns += router.urls