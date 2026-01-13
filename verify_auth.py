import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from ade.models import Store, Products, Category, Order
from django.core.files.uploadedfile import SimpleUploadedFile

def run_verification():
    print("Starting Authorization Verification...")
    
    # Setup Data
    # Ensure groups exist (they should from setup_roles)
    customer_group = Group.objects.get(name='Customer')
    seller_group = Group.objects.get(name='Seller')
    
    # Create Category
    category, _ = Category.objects.get_or_create(name='Test Category')

    # Create Users
    seller_user, _ = User.objects.get_or_create(username='seller_test', email='seller@test.com')
    seller_user.set_password('password')
    seller_user.save()
    seller_user.groups.add(seller_group)
    
    # Create Store for Seller
    store, _ = Store.objects.get_or_create(owner=seller_user, name='Seller Store')

    customer_user, _ = User.objects.get_or_create(username='customer_test', email='customer@test.com')
    customer_user.set_password('password')
    customer_user.save()
    customer_user.groups.add(customer_group)
    
    # Initialize Client
    client = APIClient()
    
    # 1. Test Seller Creating Product
    print("\n--- Test 1: Seller Creating Product ---")
    client.force_authenticate(user=seller_user)
    
    image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    dummy_image = SimpleUploadedFile("test_image.gif", image_content, content_type="image/gif")

    response = client.post('/api/products/', {
        'title': 'Seller Product',
        'category': category.id,
        'price': 100.00,
        'content': 'Great product',
        'image': dummy_image
    }, format='multipart') # Need multipart for file upload

    if response.status_code == 201:
        print("PASS: Seller created product.")
        product_id = response.data['id']
    else:
        print(f"FAIL: Seller failed to create product. Status: {response.status_code}, Data: {response.data}")
        return

    # 2. Test Customer Creating Product (Should Fail)
    print("\n--- Test 2: Customer Creating Product (Should Fail) ---")
    client.force_authenticate(user=customer_user)
    response = client.post('/api/products/', {
        'title': 'Customer Product',
        'category': category.id,
        'price': 50.00,
        'content': 'Bad attempt'
    })
    if response.status_code == 403:
        print("PASS: Customer denied creating product.")
    else:
        print(f"FAIL: Customer was allowed to create product! Status: {response.status_code}")

    # 3. Test Customer Ordering Product
    print("\n--- Test 3: Customer Ordering Product ---")
    client.force_authenticate(user=customer_user)
    response = client.post('/api/orders/', {
        'product': product_id,
        'quantity': 2
    })
    if response.status_code == 201:
        print("PASS: Customer created order.")
        order_id = response.data['id']
    else:
        print(f"FAIL: Customer failed to create order. Status: {response.status_code}, Data: {response.data}")

    # 4. Test Seller Viewing their Product's Orders
    print("\n--- Test 4: Seller Viewing Orders ---")
    client.force_authenticate(user=seller_user)
    response = client.get('/api/orders/')
    # Should see the order because it's for their product
    if response.status_code == 200:
        if any(o['id'] == order_id for o in response.data):
             print(f"PASS: Seller can see order {order_id}.")
        else:
             print("FAIL: Seller cannot see the order.")
    else:
        print(f"FAIL: Seller failed to list orders. Status: {response.status_code}")

if __name__ == '__main__':
    run_verification()
