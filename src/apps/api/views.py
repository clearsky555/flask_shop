from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from src.apps.accounts.models import User
from src.apps.accounts.serializers import *
from src.apps.product.models import Product


class UserGetViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


# class UserGetFavoriteSet(ModelViewSet):
#     serializer_class = UserFavoriteSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']  # Предполагается, что вы передаете идентификатор пользователя в URL-параметре
#         user = User.objects.get(id=user_id)
#         return user.favorites.all()
#
#
# class UserAddFavorite(ModelViewSet):
#     serializer_class = UserFavoriteSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
#
#     def create(self, request, *args, **kwargs):
#         product_id = request.data.get('product_id')
#         user = request.user
#
#         product = get_object_or_404(Product, id=product_id)
#
#         user.favorites.add(product)
#
#         return Response(status=status.HTTP_201_CREATED)
#
#
# class UserRemoveFavorite(ModelViewSet):
#     serializer_class = UserFavoriteSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
#
#     def create(self, request, *args, **kwargs):
#         product_id = request.data.get('product_id')
#         user = request.user
#
#         product = get_object_or_404(Product, id=product_id)
#
#         user.favorites.remove(product)
#
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    model = User
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'message':'Wrong Old Password'}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({
                'message':'Password successfully updated!'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]


class UserUpdateAPIView(generics.UpdateAPIView):
    model = User
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user