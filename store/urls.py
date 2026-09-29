from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_page, name='cart'),
    path('cart/update/', views.cart, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('orders/', views.orders, name='orders'),
    path('orders/<str:reference>/', views.order_detail, name='order_detail'),
]