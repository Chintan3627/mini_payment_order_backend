from django.shortcuts import render

# Create your views here.
import json
import requests
import razorpay
from decimal import Decimal
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum


from .models import Product, Order
from .serializers import ProductSerializer, OrderCreateSerializer, OrderSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class GetOrderAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Order.objects.filter(user_id=user_id)

class GetOrderByRezorpayIdAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    lookup_field = "id"          # model field
    lookup_url_kwarg = "orderId" # URL param

    def get_queryset(self):
        return Order.objects.all()



class CreateOrderAPIView(generics.GenericAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()


        # create razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_paise = int(order.total_amount * Decimal('100'))
        razorpay_order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': str(order.id),
        'payment_capture': 1,
        })
        order.razorpay_order_id = razorpay_order.get('id')
        order.save()


        return Response({
        'order_id': order.id,
        'razorpay_order_id': order.razorpay_order_id,
        'amount': amount_paise,
        'currency': 'INR',
        })

class ReportsAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]


    def get(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status=Order.STATUS_PAID).aggregate(total=Sum('total_amount'))['total'] or 0
        number_of_paid = Order.objects.filter(status=Order.STATUS_PAID).count()
        number_of_pending = Order.objects.filter(status=Order.STATUS_PENDING).count()
        return Response({
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'number_of_paid_orders': number_of_paid,
        'number_of_pending_orders': number_of_pending,
        })



@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def razorpay_webhook(request):
    # Read signature + body
    # use in prodution
    # signature = request.headers.get('X-Razorpay-Signature') or \
    #             request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
    body = request.body.decode('utf-8')

    # Verify signature
    # use in prodution
    # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    
    # try:
    #     client.utility.verify_webhook_signature(body, signature, settings.RAZORPAY_KEY_SECRET)
    # except Exception:
    #     return Response({'detail': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    data = json.loads(body)
    

    # Extract payment details
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_order_id = data.get('razorpay_order_id')
    order_id = data.get('order_id')

    # Update order
    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        order.razorpay_payment_id = razorpay_payment_id
        order.status = 'PAID'
        order.save()
        try:
            url = "https://dummyjson.com/posts/add"
            payload = {
                "order_id,": order.order_id,
                "customer_email,": order.user.email,
                "status": order.status,
                "amount": order.total_amount
            }
            response = requests.post(url, json=payload)
        except Exception as e:
            print(f"Error making external API call: {e}")




    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class DestroyOrderAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        Order.objects.filter(id=self.kwargs['pk']).delete()
        return Response({'message': 'Order deleted successfully'})


