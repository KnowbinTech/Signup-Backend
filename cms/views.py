from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from setup.views import BaseModelViewSet
from setup.export import ExportData

from .models import HeroSection
from .filters import HeroSectionFilter
from .serializers import HeroSectionModelSerializer
from .serializers import HeroSectionModelSerializerGET
from rest_framework.authentication import SessionAuthentication


@extend_schema(tags=["CMS"])
class HeroSectionModelViewSet(BaseModelViewSet, ExportData):
    queryset = HeroSection.objects.all().order_by('-id')
    serializer_class = HeroSectionModelSerializer
    retrieve_serializer_class = HeroSectionModelSerializerGET
    filterset_class = HeroSectionFilter
    search_fields = ['cta_text', 'short_description']
    default_fields = [
        'title', 'cta_text', 'short_description', 'link', 'image',
    ]


@extend_schema(tags=["CMS"])
class HeroSectionCustomer(GenericViewSet, ListModelMixin):
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = HeroSection.objects.all().order_by('-id')
    serializer_class = HeroSectionModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = HeroSectionFilter
    search_fields = ['title', 'cta_text', 'short_description']


