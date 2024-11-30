from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max
from transaction.mixins import ShipRocket


class ShipRocketViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'], url_path='orders')
    def order_list(self, request, *args, **kwargs):
        data = ShipRocket().get_all_orders()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='order/(?P<order>.*?)/details')
    def order_details(self, request, order, *args, **kwargs):
        data = ShipRocket().get_order_details(order)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='shipments')
    def shipment_list(self, request, *args, **kwargs):
        data = ShipRocket().get_all_shipment()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='shipment/(?P<shipment>.*?)/details')
    def shipment_details(self, request, shipment, *args, **kwargs):
        data = ShipRocket().get_shipment_details(shipment)
        return Response(data, status=status.HTTP_200_OK)


class ShipRocketUtility:

    def create_order(self, obj):
        """
            To Create payload and calling api to create order

            Parameter:
                obj (object): The object of the order.
        """

        order_items = obj.orderitems.all()

        length = str(order_items.aggregate(
            Max('product_variant__product__dimension__length')
        )['product_variant__product__dimension__length__max'])

        breadth = str(order_items.aggregate(
            Max('product_variant__product__dimension__breadth')
        )['product_variant__product__dimension__breadth__max'])

        height = str(order_items.aggregate(
            Max('product_variant__product__dimension__height')
        )['product_variant__product__dimension__height__max'])

        weight = str(order_items.aggregate(
            Max('product_variant__product__dimension__weight')
        )['product_variant__product__dimension__weight__max'])

        post_order_items = []

        for i in order_items:
            post_order_items.append({
                'name': i.product_variant.product.name,
                'selling_price': str(i.price),
                'sku': i.product_variant.product.sku,
                'units': i.quantity,
            })

        payload = {
            'order_id': obj.order_id,
            'order_date': obj.created_at.strftime("%Y-%m-%d %H:%M"),
            'pickup_location': 'Signup',
            'billing_customer_name': obj.address.full_name,
            'billing_last_name': '',
            'billing_address': "{},{}".format(obj.address.address_line_1, obj.address.address_line_1),
            'billing_address_2': '',
            'billing_city': obj.address.district,
            'billing_pincode': obj.address.pin_code,
            'billing_state': obj.address.state,
            'billing_country': obj.address.country if obj.address.country else 'INDIA',
            'billing_email': obj.address.user.email,
            'billing_phone': '7994977797',
            'shipping_is_billing': True,
            'order_items': post_order_items,
            'payment_method': "Prepaid",
            'shipping_charges': 0,
            'giftwrap_charges': 0,
            'transaction_charges': 0,
            'total_discount': 0,
            'sub_total': str(obj.total_amount),
            'length': '20',
            'breadth': '20',
            'height': '10',
            'weight': '2.5'
        }

        ship_rocket = ShipRocket()
        import logging

        logger = logging.getLogger('django')
        logger.error(f"This is a test error message. :  {payload}", )

        print('------------------------------------------')
        print('payload : ', payload)
        print('------------------------------------------')

        data = ship_rocket.create_order(payload)
        shipment_id = data.get('shipment_id')
        obj.shipping_id = shipment_id
        ship_rocket.request_for_shipment(shipment_id)
        return data



