from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('submit-order/', views.submit_order, name='submit-order'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('paypal-capture/', views.paypal_capture, name='paypal-capture'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
