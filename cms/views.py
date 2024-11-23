from rest_framework.decorators import action
from rest_framework.response import Response

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

from setup.utils import upload_image_to_wasabi


class HeroSectionModelViewSet(BaseModelViewSet, ExportData):
    queryset = HeroSection.objects.all().order_by('-id')
    serializer_class = HeroSectionModelSerializer
    retrieve_serializer_class = HeroSectionModelSerializerGET
    filterset_class = HeroSectionFilter
    search_fields = ['cta_text', 'short_description']
    default_fields = [
        'title', 'cta_text', 'short_description', 'link', 'image',
    ]

    @action(detail=False, methods=['post'], url_path='create_record')
    def create_record(self, request, *args, **kwargs):
        """
        Handles the creation of a new record, including logo upload.
        Parameters:
            request (HttpRequest): The HTTP request object containing model data.
        Returns:
            Response: A DRF Response object with the creation status.
        """
        serializer = self.get_serializer(data=request.data)
        image = request.data.get('image')
        if image:
            # Upload the logo to Wasabi
            image_url = upload_image_to_wasabi(image)  # Call the global function
            if image_url:
                # Append the URL to the serializer data
                key = image_url['key']
                serializer.initial_data['image'] = key
        serializer.is_valid(raise_exception=True)
        self.perform_db_action(serializer, 'create')
        return Response(serializer.data, status=201)


class HeroSectionCustomer(GenericViewSet, ListModelMixin):
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)
    queryset = HeroSection.objects.all().order_by('-id')
    serializer_class = HeroSectionModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = HeroSectionFilter
    search_fields = ['title', 'cta_text', 'short_description']


