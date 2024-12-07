from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from setup.permissions import IsCustomer

from customer.models import Cart
from product.models import Variant

from customer.serializers import CartModelSerializer
from customer.serializers import UpdateCartProductSerializer
from customer.serializers import AddToCartSerializer


@extend_schema(tags=["Customer"])
class CartModelViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Cart.objects.filter(is_completed=False)
    serializer_class = CartModelSerializer
    default_fields = [
        'user',
        'total_amount',
        'currency'
    ]

    @action(detail=False, methods=['GET'], url_path='user-cart')
    def get_cart(self, request):
        """
            Get the current user cart.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A DRF Response object indicating success or failure and a message with cart details.
        """

        cart = Cart.get_user_cart()
        return Response(CartModelSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='add-to-cart', serializer_class=AddToCartSerializer)
    def add_to_cart(self, request, *args, **kwargs):
        """
            Add a product to cart.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                product_variant (int): The primary key of the variant model.
                quantity (int): The quantity of the product to be added to the cart.
                price (Decimal): The price of the variant product.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        cart = Cart.get_user_cart(set_total=False)
           # Check if cart is None
        if cart is None:
            # Handle the case where the cart could not be created
            return Response({"error": "Cart could not be created."}, status=400)

        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)

        # Reduce the stock of the product variant
        product_variant = serializer.validated_data.get('product_variant')
        quantity = serializer.validated_data.get('quantity')
        variant = Variant.objects.get(pk=product_variant.id)
        variant.stock -= quantity
        variant.save()

        return Response({
            'data': serializer.data,
            'message': 'Successfully added to the cart.!'
        })

    @action(detail=False, methods=['POST'], url_path='update-cart-product', serializer_class=UpdateCartProductSerializer)
    def update_cart_product(self, request, *args, **kwargs):
        """
            Update the quantity of a cart product.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                product_variant (int): The primary key of the variant model.
                quantity (int): The quantity of the product to be updated to the cart.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """

        cart = Cart.get_user_cart(set_total=False)
        serializer = UpdateCartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_variant = serializer.validated_data.get('product_variant')
        quantity = serializer.validated_data.get('quantity')

        cart_item = cart.cartitems.get(
            cart=cart, product_variant=product_variant
        )
        cart_item.quantity += quantity
        cart_item.save()
        Variant.objects.get(pk=product_variant.id).update_stock(quantity)

        return Response({
            'data': serializer.data,
            'message': 'Successfully added to the cart.!'
        })

    @action(detail=False, methods=['DELETE'], url_path='(?P<pk>.*?)/remove-cart')
    def delete_from_cart(self, request, pk, *args, **kwargs):
        """
            Delete the product from the cart.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the cart item.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """

        cart = Cart.get_user_cart(set_total=False)
        item = cart.cartitems.get(id=pk)
        item.delete()
        return Response({
            'message': 'Successfully removed..!',
        }, status=status.HTTP_200_OK)



