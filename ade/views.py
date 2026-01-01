from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Category, Contact, FAQ
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home_view(request):
    featured_products = Products.objects.all().order_by('-created_at')[:4]
    return render(request, 'index.html', {'featured_products': featured_products})

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if password1 == password2:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.save()
            return redirect('login')
        
    return render(request, 'create_user.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            return redirect('login')
        
    return render(request, 'login.html')

@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Products, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    product_id = str(pk)
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'title': product.title,
            'price': float(product.price),
            'quantity': quantity,
            'image': product.image.url if product.image else ''
        }
    
    request.session.modified = True
    return redirect('products')

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id, item_data in cart.items():
        total = item_data['price'] * item_data['quantity']
        total_price += total
        item_data['total'] = total
        cart_items.append(item_data)
    
    order_lines = [f"{item['title']} (x{item['quantity']}) - {item['total']}" for item in cart_items]
    order_lines.append(f"Total: {total_price}")
    order_summary = "\n".join(order_lines)
        
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price, 'order_summary': order_summary})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')


def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        data = Contact.objects.create(name=name, email=email, message=message)
        data.save()
        return redirect('contact')
    return render(request, 'contact.html')


def product_view(request):
    products = Products.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    return render(request, 'products.html', {'products': products, 'categories': categories})

def product_detail_view(request, pk):
    product = Products.objects.get(pk=pk)
    return render(request, 'detail.html', {'product': product})  


def faq_view(request):
    faqs = FAQ.objects.all().order_by('-created_at')    
    return render(request, 'faq.html', {'faq': faqs})

