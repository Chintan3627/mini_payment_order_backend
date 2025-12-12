from django.urls import path
from .views import (ProductListAPIView, CreateOrderAPIView, ReportsAPIView, 
                    razorpay_webhook,GetOrderAPIView,GetOrderByRezorpayIdAPIView,
                    DestroyOrderAPIView)


urlpatterns = [
path('products/', ProductListAPIView.as_view(), name='product-list'),
path('orders/create/', CreateOrderAPIView.as_view(), name='order-create'),
path('orders/<int:user_id>/', GetOrderAPIView.as_view(), name='order-create'),
path('orders/delete/<int:pk>/', DestroyOrderAPIView.as_view(), name='order-create'),
path('reports/', ReportsAPIView.as_view(), name='reports'),
path('payments/webhook/', razorpay_webhook, name='razorpay-webhook'),
path('orders/razorpay/<int:orderId>/', GetOrderByRezorpayIdAPIView.as_view(), name='razorpay-webhook'),

]