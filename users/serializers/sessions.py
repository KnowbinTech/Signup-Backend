import requests
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from users.models.other import AddressRegister
from setup.logto import LOGTOManagementAPI


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user = authenticate(requests, username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials... Please re enter your Username and Password.')

        # noinspection PyAttributeOutsideInit
        self.user = user
        return validated_data

    def login(self, request):
        if hasattr(self, 'user') is False:
            raise Exception('The user is not authenticated.')
        login(request, self.user)
        return self.user


class ResetPassword(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        from setup.middleware.request import CurrentRequestMiddleware
        request_user = CurrentRequestMiddleware.get_request().user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'new_password': "Password doesn't match"
                }
            )

        self.logto = LOGTOManagementAPI() # noqa

        try:
            self.logto.user_has_password(request_user.sub)
        except Exception as e:
            print('Exception : ', e)
            raise serializers.ValidationError('Invalid password.')

        try:
            self.logto.check_password(request_user.sub, old_password)
        except Exception as e:
            print('Exception : ', e)
            raise serializers.ValidationError('Invalid password.')

        self.user = request_user # noqa

        return attrs

    def save(self, password):
        try:
            self.logto.change_password(self.user.sub, password)
        except Exception as e:
            raise serializers.ValidationError("Something went wrong, Please try again later.!")


class AddressRegisterModelSerializer(serializers.ModelSerializer):
    def clean(self, attrs):
        pass

    class Meta:
        model = AddressRegister
        fields = '__all__'


