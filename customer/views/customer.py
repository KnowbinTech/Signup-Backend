from rest_framework.viewsets import GenericViewSet
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
from django_filters.rest_framework import DjangoFilterBackend

from masterdata.models import Brand
from product.models import Products
from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from orders.models import Order

from product.serializers import ProductsModelSerializerGET
from product.serializers import VariantModelSerializerGET
from product.serializers import CollectionModelSerializerGET
from product.serializers import LookBookModelSerializerGET
from product.serializers import BrandSerializerGET
from orders.serializers import OrderItemsModelSerializerGET

from masterdata.serializers import CategoryModelSerializerGET

from customer.filters import CustomerProductFilter
from customer.filters import CustomerVariantFilter
from customer.filters import CustomerCategoryFilter
from customer.filters import CustomerCollectionFilter
from customer.filters import CustomerLookBookFilter
from customer.filters import CustomerOrderFilter
from rest_framework.authentication import SessionAuthentication


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
    queryset = Products.objects.all().order_by('-id')
    serializer_class = ProductsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerProductFilter
    search_fields = ['name', 'brand__name']

    def get_queryset(self):
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

    # def list(self, request, *args, **kwargs):
    #     query = request.query_params.get('query', '')
    #     search_results = raw_search(Variant, query)  # Query Algolia index
    #     serializer = self.get_serializer(search_results, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


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
