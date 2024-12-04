from drf_spectacular.utils import extend_schema
from setup.views import BaseModelViewSet
from users.models import User
from users.serializers import StoreManagerModelSerializer
from users.serializers import UserModelSerializerGET


@extend_schema(tags=["Account"])
class ManagerViewSet(BaseModelViewSet):
    queryset = User.objects.filter(deleted=False)
    serializer_class = StoreManagerModelSerializer
    retrieve_serializer_class = UserModelSerializerGET
    default_fields = [
        'username', 'name', 'last_name',
        'email', 'mobile_number'
    ]
    search_fields = [
        'username', 'name', 'email', 'mobile_number'
    ]

    # def perform_db_action(self, serializer, action='create'):
    #     if action == 'create':
    #         pass



