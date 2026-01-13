from rest_framework import serializers
from .models import Products, Category, Store, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'owner', 'name', 'description', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    class Meta:
        model = Products
        fields = ['id', 'store', 'title', 'category', 'image', 'price', 'content', 'created_at', 'updated_at']
        read_only_fields = ['store', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assign the store of the current user
        user = self.context['request'].user
        if hasattr(user, 'store'):
            validated_data['store'] = user.store
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_details', 'quantity', 'total_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'total_price', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        product = validated_data['product']
        validated_data['total_price'] = product.price * validated_data.get('quantity', 1)
        return super().create(validated_data)
