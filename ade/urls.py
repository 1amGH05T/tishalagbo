from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.create_user, name='create_user'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('products/', views.product_view, name='products'),
    path('products/<int:pk>/', views.product_detail_view, name='detail'),
    path('faq/', views.faq_view, name='faq'), 
]
