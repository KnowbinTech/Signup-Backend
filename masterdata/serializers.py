from rest_framework import serializers

from .models import Category
from .models import Brand
# from .models import Tag
from .models import Attribute
from .models import AttributeGroup
from .models import Dimension
from .models import ReturnReason
from setup.utils import generate_presigned_url


class BrandModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    logo = serializers.FileField(required=False)
    description = serializers.CharField(required=True)
    is_active = serializers.BooleanField(default=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)

    class Meta:
        model = Brand
        exclude = (
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
            'deleted',
            'deleted_at',
            'deleted_by',
        )
    
    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Brand.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Brand.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class BrandModelSerializerGET(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_logo(self, attrs):
        return attrs.logo.url if attrs.logo else ''

    class Meta:
        model = Brand
        fields = '__all__'


class AttributeModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    value = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Attribute.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Attribute.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs

    class Meta:
        model = Attribute
        fields = (
            'name',
            'value',
        )


class RetrieveAttributeModelSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeGroupModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if AttributeGroup.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if AttributeGroup.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs

    class Meta:
        model = AttributeGroup
        fields = (
            'name',
            'attributes',
        )

    def create(self, validated_data):
        attributes = validated_data.pop('attributes', None)

        attribute_group = AttributeGroup.objects.create(**validated_data)

        if attributes:
            attribute_group.attributes.set(attributes)

        return attribute_group


class RetrieveAttributeGroupModelSerializer(serializers.ModelSerializer):
    attributes = RetrieveAttributeModelSerializer(many=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = AttributeGroup
        fields = '__all__'


class DimensionModelSerializer(serializers.ModelSerializer):
    length = serializers.DecimalField(max_digits=10, decimal_places=2)
    breadth = serializers.DecimalField(max_digits=10, decimal_places=2)
    height = serializers.DecimalField(max_digits=10, decimal_places=2)
    dimension_unit = serializers.ChoiceField(choices=Dimension.DIMENSION_UNIT)
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = serializers.ChoiceField(choices=Dimension.WEIGHT_UNIT)

    class Meta:
        model = Dimension
        fields = (
            'length',
            'breadth',
            'height',
            'dimension_unit',
            'weight',
            'weight_unit',
        )


class RetrieveDimensionModelSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Dimension
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    image = serializers.FileField(required=False)
    handle = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)

    def validate(self, attrs):
        name = attrs.get('name')
        handle = attrs.get('handle')

        if not self.instance:
            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

            if Category.objects.filter(handle=handle).exists():
                raise serializers.ValidationError({
                    'name': 'Handle is already in use.'
                })

        else:
            if name != self.instance.name:
                if Category.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

            if handle != self.instance.handle:
                if Category.objects.filter(handle=handle).exists():
                    raise serializers.ValidationError({
                        'name': 'Handle is already in use.'
                    })

        return attrs

    class Meta:
        model = Category
        fields = (
            'name',
            'description',
            'handle',
            'is_active',
            'parent_category',
            'attribute_group',
            'tags',
            'image',
            'is_main_menu',
            'is_top_category',
        )


class CategoryModelSerializerGET(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    attribute_group = RetrieveAttributeGroupModelSerializer()
    image = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    parent_category = serializers.SerializerMethodField()

    def get_parent_category(self, attrs):
        return {'id':attrs.parent_category.id, 'name':attrs.parent_category.name} if attrs.parent_category else ''

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_image(self, attrs):
        return attrs.image.url if attrs.image else ''


    def get_sub_category(self, attrs):
        return CategoryModelSerializerGET(attrs.subcategory.all(), many=True).data

    class Meta:
        model = Category
        fields = '__all__'


class CategoryGET(serializers.ModelSerializer):
    attribute_group = RetrieveAttributeGroupModelSerializer()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Category
        fields = '__all__'


class ReturnReasonModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = ReturnReason
        fields = (
            'title',
            'description',
        )


class ReturnReasonModelSerializerGET(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = ReturnReason
        fields = '__all__'

