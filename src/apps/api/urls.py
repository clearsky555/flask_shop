from django.urls import path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


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
]