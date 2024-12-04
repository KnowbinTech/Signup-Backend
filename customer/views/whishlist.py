from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

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


class WishListModelViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = WishList.objects.all()
    serializer_class = WishListGETSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = wishListFilter
    search_fields = ['name', 'brand__name']

    @action(detail=False, methods=['POST'], url_path='wishlist-product', serializer_class=WishListModelSerializer)
    def toggle_wishlist(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('id')

        if not product_id:
            return Response({
                'message': 'Product ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            wishlist_item = WishList.objects.filter(user__pk=user.id, product_id=product_id).first()
            if wishlist_item:
                wishlist_item.delete()
                return Response({
                    'is_wishlisted' : False,
                    'message': 'Removed from Wishlist.'
                }, status=status.HTTP_200_OK)
            else:
                # Pass the user to the serializer's context
                serializer = WishListModelSerializer(data={'product': product_id}, context={'user': user})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    'is_wishlisted' : True,
                    'message': 'Added to Wishlist.'
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': 'Error toggling Wishlist.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


