from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from src.apps.product.serializers import *
from src.apps.product.models import *


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []  # Add your desired permission classes for read-only actions
        else:
            permission_classes = [IsAuthenticated]  # Add your desired permission classes for other actions (e.g., create, update, delete)

        return [permission() for permission in permission_classes]