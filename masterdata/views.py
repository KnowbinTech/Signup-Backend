from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from setup.views import BaseModelViewSet
from setup.export import ExportData

from .models import Category
from .models import Brand
from .models import Attribute
from .models import AttributeGroup
from .models import Dimension
from .models import ReturnReason
from product.models import Products

from .serializers import CategoryModelSerializer
from .serializers import CategoryModelSerializerGET
from .serializers import BrandModelSerializer
from .serializers import BrandModelSerializerGET
from .serializers import AttributeModelSerializer
from .serializers import RetrieveAttributeModelSerializer
from .serializers import AttributeGroupModelSerializer
from .serializers import RetrieveAttributeGroupModelSerializer
from .serializers import DimensionModelSerializer
from .serializers import RetrieveDimensionModelSerializer
from .serializers import ReturnReasonModelSerializer
from .serializers import ReturnReasonModelSerializerGET

from .filters import CategoryFilter
from .filters import BrandFilter
from .filters import AttributeGroupFilter
from django.shortcuts import get_object_or_404



class CategoryModelViewSet(BaseModelViewSet, ExportData):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategoryModelSerializer
    retrieve_serializer_class = CategoryModelSerializerGET
    search_fields = ['name', 'parent_category__name', 'description']
    default_fields = [
        'name', 'description', 'is_active', 'parent_category',
        'second_parent_category', 'attribute_group'
    ]
    filterset_class = CategoryFilter


    @action(detail=True, methods=['POST'], url_path='deactivate')
    def deactivate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deactivate()

        return Response({
            'message': f'{obj.name} successfully deactivated.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='activate')
    def activate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.activate()

        return Response({
            'message': f'{obj.name} successfully activated.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'])
    def delete_record(self, request, *args, **kwargs):
        # Retrieve the specific attribute instance
        category = get_object_or_404(Category, pk=kwargs.get('pk'))

        id = kwargs.get('pk')  # This should give you '1' in this case

        if Products.objects.filter(categories=id, deleted=False).exists():
            return Response(
            {
                'message': 'Cannot delete category. It is linked to one or more Products.'
            },
            status=status.HTTP_200_OK
            )
        
        category.deleted = True
        category.save()
        return Response(
            {
                'message': 'Category has been deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

class BrandModelViewSet(BaseModelViewSet, ExportData):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    retrieve_serializer_class = BrandModelSerializerGET
    search_fields = ['name']
    default_fields = ['name', 'description']
    filterset_class = BrandFilter

    @action(detail=True, methods=['POST'], url_path='deactivate')
    def deactivate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deactivate()

        return Response({
            'message': f'{obj.name} successfully deactivated.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='activate')
    def activate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.activate()

        return Response({
            'message': f'{obj.name} successfully activated.!'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['DELETE'])
    def delete_record(self, request, *args, **kwargs):
        
        brand = get_object_or_404(Brand, pk=kwargs.get('pk'))

        id = kwargs.get('pk')  # This should give you '1' in this case

        if Products.objects.filter(brand=id, deleted=False).exists():
            return Response(
            {
                'message': 'Cannot delete brand. It is linked to one or more Products.'
            },
            status=status.HTTP_200_OK
            )
        
        brand.deleted = True
        brand.save()
        return Response(
            {
                'message': 'Brand has been deleted successfully.'
            },
            status=status.HTTP_200_OK
        )


class AttributeModelViewSet(BaseModelViewSet, ExportData):
    queryset = Attribute.objects.all()
    serializer_class = AttributeModelSerializer
    retrieve_serializer_class = RetrieveAttributeModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'value']

        
    @action(detail=True, methods=['DELETE'])
    def delete_record(self, request, *args, **kwargs):
        # Retrieve the specific attribute instance
        attribute = get_object_or_404(Attribute, pk=kwargs.get('pk'))

        id = kwargs.get('pk')  # This should give you '1' in this case

        if AttributeGroup.objects.filter(attributes=id, deleted=False).exists():
            return Response(
            {
                'message': 'Cannot delete attribute. It is linked to one or more AttributeGroups.'
            },
            status=status.HTTP_200_OK
            )
        
        attribute.deleted = True
        attribute.save()
        return Response(
            {
                'message': 'Attribute has been deleted successfully.'
            },
            status=status.HTTP_200_OK
        )


class AttributeGroupModelViewSet(BaseModelViewSet, ExportData):
    queryset = AttributeGroup.objects.all()
    serializer_class = AttributeGroupModelSerializer
    retrieve_serializer_class = RetrieveAttributeGroupModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'attributes']
    filterset_class = AttributeGroupFilter

    @action(detail=True, methods=['DELETE'])
    def delete_record(self, request, *args, **kwargs):
        # Retrieve the specific attribute instance
        attribute_group = get_object_or_404(AttributeGroup, pk=kwargs.get('pk'))

        id = kwargs.get('pk')  # This should give you '1' in this case

        if Category.objects.filter(attribute_group_id=id, deleted=False).exists():
            return Response(
            {
                'message': 'Cannot delete attribute group. It is linked to one or more Categories.'
            },
            status=status.HTTP_200_OK
            )
        
        attribute_group.deleted = True
        attribute_group.save()
        return Response(
            {
                'message': 'Attribute Group has been deleted successfully.'
            },
            status=status.HTTP_200_OK
        )


class DimensionModelViewSet(BaseModelViewSet, ExportData):
    queryset = Dimension.objects.all()
    serializer_class = DimensionModelSerializer
    retrieve_serializer_class = RetrieveDimensionModelSerializer
    search_fields = ['length']
    default_fields = [
        'length', 'breadth', 'height',
        'dimension_unit', 'weight', 'weight_unit'
    ]


class ReturnReasonModelViewSet(BaseModelViewSet, ExportData):
    queryset = ReturnReason.objects.all()
    serializer_class = ReturnReasonModelSerializer
    retrieve_serializer_class = ReturnReasonModelSerializerGET
    search_fields = ['title']
    default_fields = [
        'title', 'description',
    ]



