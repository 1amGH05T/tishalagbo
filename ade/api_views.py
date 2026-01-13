from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Products, Order, Store, Category
from .serializers import ProductSerializer, OrderSerializer, StoreSerializer, CategorySerializer, UserSerializer
from .permissions import IsSeller, IsCustomer, IsOwnerOrReadOnly, IsStoreOwner

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSeller, IsStoreOwner]
            # Since IsStoreOwner checks obj.store.owner, we also need to ensure the user IS a seller.
            # But for 'create', there is no object yet.
            if self.action == 'create':
                permission_classes = [IsSeller]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(store=self.request.user.store)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Customer').exists():
            return Order.objects.filter(user=user)
        elif user.groups.filter(name='Seller').exists():
            if hasattr(user, 'store'):
                return Order.objects.filter(product__store=user.store)
        elif user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsCustomer]
        else:
            permission_classes = [permissions.IsAuthenticated]
            # Further restriction is done in get_queryset
        return [permission() for permission in permission_classes]

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreOwner]

    def get_queryset(self):
        # Users can only see their own store in this viewset maybe?
        # Or public can see stores? Let's assume public can see, owner can edit.
        return Store.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsStoreOwner()]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
