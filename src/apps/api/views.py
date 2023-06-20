from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView

from src.apps.accounts.models import User
from src.apps.accounts.serializers import *
from src.apps.product.models import Product
from src.apps.product.serializers import ProductSerializer

from src.apps.cart.cart import Cart


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


class AddFavoriteProduct(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        if product not in user.favorites.all():
            user.favorites.add(product)
            return Response(
                {'message':'Product was added to favorites'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message':'Product is already in favorites'},
            status=status.HTTP_200_OK
        )


class RemoveFavoriteProduct(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        if product in user.favorites.all():
            user.favorites.remove(product)
            return Response(
                {'message':'Product was removed from favotites'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message':'Product is not in favorites'},
            status=status.HTTP_200_OK
        )


class UserProductFavoritesList(generics.ListAPIView):
    serializer_class = ProductSerializer
    model = Product
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        products = user.favorites.all()
        return products


@api_view(['POST'])
def add_cart(request, pk):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        cart.add(product)
        return Response({'message':'ok'}, status=200)
    return Response({'message':'Not allowed method'}, status=400)


@api_view(['POST'])
def minus_cart(request, pk):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        cart.minus(product)
        return Response({'message':'ok'}, status=200)
    return Response({'message':'Not allowed method'}, status=400)