from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from setup.permissions import IsCustomer

from customer.models import WishList

from customer.serializers.serializers import WishListModelSerializer
from customer.serializers.serializers import WishListGETSerializer
from customer.filters import wishListFilter


@extend_schema(tags=["Customer"])
class WishListModelViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = WishList.objects.all().order_by('-id')
    serializer_class = WishListGETSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = wishListFilter
    search_fields = ['name', 'brand__name']

    @action(detail=False, methods=['POST'], url_path='add-to-wishlist', serializer_class=WishListModelSerializer)
    def add_to_wishlist(self, request, *args, **kwargs):
        user = request.user
        serializer = WishListModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response({
            'data': serializer.data,
            'message': 'Successfully added to wishlist.!'
        })

    @action(detail=False, methods=['DELETE'], url_path='(?P<pk>.*?)/remove-wishlist')
    def delete_from_cart(self, request, pk, *args, **kwargs):
        try:
            user = request.user
            item = user.user_wishlist.get(product_variant_id=pk)
            item.delete()
        except Exception as e:
            return Response({
                'message': 'Error remove wishlist',
                'error': e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'message': 'Successfully removed..!',
        }, status=status.HTTP_200_OK)

