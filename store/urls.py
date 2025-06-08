from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('', views.home, name='home'),
    path('submit-order/', views.submit_order),
    path('stripe/webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('paypal-capture', views.paypal_capture),
    path('success', views.success),
    path('cancel/', views.cancel),
    path('categories/', views.CategoryList.as_view()),
    path("products/<int:pk>/", views.ProductDetail.as_view())

]
