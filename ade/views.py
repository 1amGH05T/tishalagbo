from django.shortcuts import render, redirect
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
            return redirect('login_user')
        
    return render(request, 'create_user.html')


def login_user(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login_user')
        
    return render(request, 'login.html')


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

