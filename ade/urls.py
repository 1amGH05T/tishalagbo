from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r'stores', api_views.StoreViewSet)
router.register(r'categories', api_views.CategoryViewSet)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.create_user, name='create_user'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('products/', views.product_view, name='products'),
    path('products/<int:pk>/', views.product_detail_view, name='detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('faq/', views.faq_view, name='faq'), 
    
    # API Endpoints
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
