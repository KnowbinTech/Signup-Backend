from rest_framework import serializers

from .models import HeroSection

from setup.utils import generate_presigned_url


class HeroSectionModelSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)

    class Meta:
        model = HeroSection
        fields = (
            'title',
            'image',
            'short_description',
            'cta_text',
            'is_in_shop_page',
            'link',
        )


class HeroSectionModelSerializerGET(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_image(self, attrs):
        return attrs.image.url if attrs.image else ''

    class Meta:
        model = HeroSection
        fields = '__all__'
