from rest_framework import serializers
from users.models import User


class StoreManagerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'mobile_number',
            'date_of_birth',
            'profile_picture',
        )

