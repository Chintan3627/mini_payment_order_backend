from rest_framework import serializers
from .models import Product, Order, OrderItem
from auth_flow.models import CustomUser

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','sku','description','price','available']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = OrderItem
        fields = ['id','product','product_id','quantity','unit_price']


class OrderItemValidator(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    items = serializers.ListField(
        child=OrderItemValidator()
    )


    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('Order must contain at least one item.')
        return value


    def create(self, validated_data):
        from .models import Product
        items_data = validated_data.pop('items')

        custom_user_obj = CustomUser.objects.filter(pk=validated_data['user']).last()
        order_created_data = {
            'user': custom_user_obj,
            'customer_email': custom_user_obj.email if custom_user_obj else None
        }
        
        
        order = Order.objects.create(**order_created_data)
        total = 0
        for it in items_data:
            product = Product.objects.get(pk=it['product'])
            quantity = int(it.get('quantity',1))
            unit_price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=unit_price)
            total += unit_price
        order.total_amount = total
        order.save()
        return order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)


    class Meta:
        model = Order
        fields = ['id','order_id','customer_email','total_amount','status','created_at','razorpay_order_id','razorpay_payment_id','items']
