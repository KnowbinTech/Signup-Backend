from rest_framework import serializers

from customer.models import Cart
from customer.models import CartItem
from customer.models import WishList
from customer.models import Review
from customer.models import ReviewImage
from product.models import Variant

from users.serializers import UserDataModelSerializer


class CartModelSerializer(serializers.ModelSerializer):
    user = UserDataModelSerializer()
    items = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_items(self, attrs):
        items = attrs.cartitems.all()
        return CartItemModelSerializer(items, many=True).data

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemModelSerializer(serializers.ModelSerializer):
    product_variant = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_product_variant(self, attrs):
        from product.serializers import VariantModelSerializerGET
        return VariantModelSerializerGET(attrs.product_variant).data

    class Meta:
        model = CartItem
        fields = '__all__'


class AddToCartSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = (
            'product_variant',
            'quantity',
            'price',
        )

    def validate(self, attrs):
        product_variant = attrs.get('product_variant')
        quantity = attrs.get('quantity')

        if quantity < 1:
            raise serializers.ValidationError({
                'quantity': 'Quantity must be 1 or above.!'
            })

        if product_variant.stock < quantity:
            raise serializers.ValidationError({
                'product_variant': 'Only have limited stock.!'
            })

        return attrs

    def create(self, validated_data):
        cart = validated_data.pop('cart')
        product_variant = validated_data.get('product_variant')
        validated_quantity = validated_data.get('quantity')
        price = validated_data.get('price')
        try:
            obj = CartItem.objects.get(
                cart=cart, product_variant=product_variant
            )
            quantity = obj.quantity if obj.quantity else 0
            obj.quantity = quantity + validated_quantity
            obj.price = price
            obj.save()
        except CartItem.DoesNotExist:
            obj = CartItem.objects.create(cart=cart, **validated_data)

        return obj


class UpdateCartProductSerializer(serializers.Serializer):
    product_variant = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Variant.objects.all(),
        required=True,
    )
    quantity = serializers.IntegerField(min_value=-1, max_value=1)

    def validate(self, attrs):
        product_variant = attrs.get('product_variant')
        quantity = attrs.get('quantity')

        obj = Variant.objects.get(pk=product_variant.id)
        if obj.stock < 0:
            raise serializers.ValidationError({
                'quantity': 'Out of Stock'
            })

        return attrs


class WishListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = (
            'product',
        )

    def create(self, validated_data):
        user = self.context.get('user') or validated_data.pop('user', None)
        if not user:
            raise serializers.ValidationError({'user': 'User not Authenticated.'})

        obj, created = WishList.objects.get_or_create(user=user, **validated_data)
        return obj


class WishListGETSerializer(serializers.ModelSerializer):
    user = UserDataModelSerializer()
    product = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_product_variant(self, attrs):
        from product.serializers import VariantModelSerializerGET
        return VariantModelSerializerGET(attrs.product_variant).data

    class Meta:
        model = WishList
        fields = '__all__'


class ReviewSerializerPOST(serializers.ModelSerializer):
    review_images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Review
        fields = (
            'product',
            'comment',
            'rating',
            'review_images'
        )

    def create(self, validated_data):
        review_images = validated_data.pop('review_images', [])
        review = Review.objects.create(**validated_data)

        for image in review_images:
            review.review_image.create(**{
                'file': image,
                'name': image.name
            })

        return review


class ReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_images(self, attrs):
        return ReviewImageSerializer(ReviewImage.objects.filter(review_id=attrs.id), many=True).data

    class Meta:
        model = Review
        fields = '__all__'


class ReviewImageSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = ReviewImage
        fields = '__all__'