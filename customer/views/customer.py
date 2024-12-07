from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Prefetch

from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.db.models import Count

from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication

from masterdata.models import Brand
from masterdata.models import Category
from masterdata.serializers import CategoryModelSerializerGET

from product.models import Products
from product.models import ProductImage
from product.models import Variant
from product.models import VariantAttributes
from product.models import Collection
from product.models import LookBook
from product.serializers import ProductsModelSerializer
from masterdata.models import Category
from orders.models import Order

from product.serializers import ProductsModelSerializerGET
from product.serializers import VariantModelSerializerGET
from product.serializers import CollectionModelSerializerGET
from product.serializers import LookBookModelSerializerGET
from product.serializers import BrandSerializerGET

from orders.models import Order
from orders.serializers import OrderItemsModelSerializerGET


from customer.filters import CustomerProductFilter
from customer.filters import CustomerVariantFilter
from customer.filters import CustomerCategoryFilter
from customer.filters import CustomerCollectionFilter
from customer.filters import CustomerLookBookFilter
from customer.filters import CustomerOrderFilter
from customer.models import WishList


@extend_schema(tags=["Customer"])
class CustomerProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
        Get the list of variant products.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the variant product data.
    """
    # authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Products.objects.all()
    serializer_class = ProductsModelSerializerGET
    retrieve_serializer_class = ProductsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerProductFilter
    search_fields = ['name', 'brand__name']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' and self.retrieve_serializer_class:
            return self.retrieve_serializer_class
        return self.serializer_class

    def get_queryset(self, *args, **kwargs):
        """
        Exclude products with no variants.
        """
        return Products.objects.annotate(variant_count=Count('product_variant')).filter(variant_count__gt=0)

    @action(detail=True, methods=['GET'], url_path='other-variants')
    def other_variants(self, request, *args, **kwargs):
        """
            API to fetch all similar variants
        """
        obj = self.get_object()
        return Response(
            VariantModelSerializerGET(obj.product_variant.all(), many=True).data,
            status=status.HTTP_200_OK
        )

class CustomProductListView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    Optimized view to list variant products with pagination.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Products.objects.filter(deleted=False)
    serializer_class = ProductsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerProductFilter
    search_fields = ['name', 'brand__name']

    def get_queryset(self):
        """
        Optimized queryset to fetch only required fields and relationships.
        """
        queryset = (
            self.queryset.annotate(variant_count=Count('product_variant'))
            .filter(variant_count__gt=0)
            .only('id', 'name', 'brand__id', 'brand__name', 'price', 'selling_price', 'rating')
            .prefetch_related(
                Prefetch(
                    'product_images',
                    queryset=ProductImage.objects.only('id', 'image')
                ),
                Prefetch(
                    'product_variant__variant__attributes',
                    queryset=VariantAttributes.objects.only('id', 'name', 'value')
                )
            )
        )
        # Wishlist filter logic
        wishlisted = self.request.query_params.get('wishlist')
        username = self.request.query_params.get('username')
        if wishlisted and username:
            queryset = Products.objects.filter(product_wishlist__user__username=username, product_wishlist__deleted=False)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        List products with pagination and optimized data fetching.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        # Use paginated response if applicable
        product_list = [
            self.get_product_data(product) for product in (page if page is not None else queryset)
        ]
        if page is not None:
            return self.get_paginated_response(product_list)
        return Response(product_list, status=status.HTTP_200_OK)

    def get_product_data(self, product):
        """
        Build and return product data dictionary.
        """
        product_image = next(iter(product.product_images.all()), None)
        username = self.request.query_params.get('username')
        is_wishlisted = (product.product_wishlist
                 .filter(user__username=username, deleted=False)
                 .exists() if username else False)
        return {
            'id': product.id,
            'name': product.name,
            'brand': product.brand.name if product.brand else '',
            'brand_id': product.brand.id if product.brand else '',
            'price': product.price,
            'selling_price': product.selling_price,
            'image': product_image.image.url if product_image and product_image.image else '',
            'rating': product.rating or '',
            'variants': product.get_distinct_variant_attributes(),
            'is_wishlisted': is_wishlisted,
        }

class CustomerLookBookViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of products for home page listing.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the look book data.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Products.objects.all()
    serializer_class = ProductsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerProductFilter
    search_fields = ['name', 'brand__name']


@extend_schema(tags=["Customer"])
class CustomerVariantViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
        Get the list of variant products.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the variant product data.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Variant.objects.filter(product__deleted=False)
    serializer_class = VariantModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerVariantFilter
    search_fields = ['product__name', 'product__brand', 'product__tags']

    @action(detail=True, methods=['GET'], url_path='other-variants')
    def other_variants(self, request, *args, **kwargs):
        """
            API to fetch all similar variants
        """
        obj = self.get_object()
        return Response(
            VariantModelSerializerGET(obj.product.product_variant.all(), many=True).data,
            status=status.HTTP_200_OK
        )


@extend_schema(tags=["Customer"])
class CustomerCategoryViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of categories.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the category data.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Category.objects.filter(parent_category__isnull=True).order_by('name')
    serializer_class = CategoryModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerCategoryFilter
    search_fields = ['name', 'tags', 'handle']


@extend_schema(tags=["Customer"])
class CustomerCollectionViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of collection.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the collection data.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Collection.objects.all().order_by('-id')
    serializer_class = CollectionModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerCollectionFilter
    search_fields = ['name', 'tags', 'description']


@extend_schema(tags=["Customer"])
class CustomerLookBookViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of look book.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the look book data.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = LookBook.objects.all().order_by('-id')
    serializer_class = LookBookModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerLookBookFilter
    search_fields = ['name']


@extend_schema(tags=["Customer"])
class CustomerOrderViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of Orders.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the look book data.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerOrderFilter
    search_fields = ['order_id']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user.username)


@extend_schema(tags=["Customer"])
class CustomerBrandViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    Get the list of brands.
     Parameters:
        request (HttpRequest): The HTTP request object containing model data.
     Returns:
        Response: A DRF Response object with the brand data.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = Brand.objects.all().order_by('-id')
    serializer_class = BrandSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']

    @action(detail=True, methods=['GET'], url_path='products')
    def brand_products(self, request, *args, **kwargs):
        """
        API to fetch all products for a specific brand
        """
        brand = self.get_object()
        products = Products.objects.filter(brand=brand)
        return Response(
            ProductsModelSerializerGET(products, many=True).data,
            status=status.HTTP_200_OK
        )
