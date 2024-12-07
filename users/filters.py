import django_filters as filters

from users.models import AddressRegister
from users.models import User


class AddressRegisterFilter(filters.FilterSet):
    class Meta:
        model = AddressRegister
        fields = ['user']

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ["name",'username']

