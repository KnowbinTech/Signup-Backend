from setup.views import BaseModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Inventory
from .models import Batch
from .models import Tax
from .models import Warehouse
from product.models import Products

from .serializers import InventoryModelSerializer
from .serializers import BatchModelSerializer
from .serializers import TaxModelSerializer
from .serializers import TaxModelSerializerGET
from .serializers import WarehouseModelSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404



class TaxModelViewSet(BaseModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxModelSerializer
    retrieve_serializer_class = TaxModelSerializerGET
    search_fields = ['name']
    default_fields = [
        'name',
        'slab'
    ]

    @action(detail=True, methods=['DELETE'])
    def delete_record(self, request, *args, **kwargs):
        
        tax = get_object_or_404(Tax, pk=kwargs.get('pk'))

        id = kwargs.get('pk')  # This should give you '1' in this case

        if Products.objects.filter(brand=id, deleted=False).exists():
            return Response(
            {
                'message': 'Cannot delete tax. It is linked to one or more Products.'
            },
            status=status.HTTP_200_OK
            )
        
        tax.deleted = True
        tax.save()
        return Response(
            {
                'message': 'Tax has been deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

class WarehouseModelViewSet(BaseModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseModelSerializer
    search_fields = ['name']
    default_fields = ['name']


class BatchModelViewSet(BaseModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchModelSerializer
    search_fields = ['batch_number', 'rack', 'row']
    default_fields = [
        'warehouse',
        'batch_number',
        'rack',
        'row',
        'expiry_date',
        'purchase_amount',
        'mrp',
        'selling_price',
        'purchase_quantity',
        'stock',
        'is_perishable',
        'is_disabled',
        'tax_inclusive',
        'purchase_amount_tax_inclusive',
        'tax'
    ]


class InventoryModelViewSet(BaseModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventoryModelSerializer
    search_fields = ['stock', 'batch']
    default_fields = [
        'variants',
        'stock',
        'batch',
        'low_stock_notification'
    ]
