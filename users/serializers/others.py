from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from users.models.other import AddressRegister
from users.models import User
from users.utils import convert_timestamp_to_date_time


class UserSignupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',

            'name',
            'email',
            'mobile_number',
            'date_of_birth',
            'gender',

            'profile_picture',
        )

        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSignupModelSerializer, self).validate(data)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.is_customer = True
        instance.save()
        return instance


class UserDataModelSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, attrs):
        return attrs.profile_picture.url if attrs.profile_picture else attrs.profile_picture_url or ''

    class Meta:
        model = User
        fields = (
            'username',

            'name',
            'email',
            'mobile_number',
            'date_of_birth',
            'gender',

            'profile_picture',
            'is_customer',
            'customer_id',
            'is_suspended',

            'is_superuser',
            'store_manager',
        )


class AddressRegisterModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, attrs):
        return UserDataModelSerializer(attrs.user).data

    def create(self, validated_data):
        from setup.middleware.request import CurrentRequestMiddleware
        user = CurrentRequestMiddleware.get_request().user
        obj = AddressRegister.objects.create(**validated_data)
        obj.user = user
        obj.save()
        return obj

    class Meta:
        model = AddressRegister
        exclude = (
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
            'deleted',
            'deleted_at',
            'deleted_by',
        )


class AddressRegisterModelSerializerGET(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_user(self, attrs):
        return UserDataModelSerializer(attrs.user).data

    class Meta:
        model = AddressRegister
        fields = '__all__'


class UserModelSerializerGET(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    def get_profile_picture(self, attrs):
        return attrs.profile_picture.url if attrs.profile_picture else attrs.profile_picture_url or ''

    class Meta:
        model = User
        exclude = (
            'password',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=User.GENDER, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'mobile_number',
            'date_of_birth',
            'gender',
            'profile_picture',
            'email',
        )


class NewUserSerializer(serializers.ModelSerializer):
    ip = serializers.CharField()
    event = serializers.CharField()
    hookId = serializers.CharField()
    sessionId = serializers.CharField()
    userAgent = serializers.CharField()
    application = serializers.JSONField()
    interactionEvent = serializers.CharField()
    data = serializers.JSONField()

    class Meta:
        model = User
        fields = [
            'ip',
            'event',
            'hookId',
            'sessionId',
            'userAgent',
            'application',
            'interactionEvent',
            'data',
        ]

    def create(self, validated_data):
        ip = validated_data.get('ip', None)
        event = validated_data.get('event', None)
        hookId = validated_data.get('hookId', None)
        sessionId = validated_data.get('sessionId', None)
        userAgent = validated_data.get('userAgent', None)
        application = validated_data.get('application', None)
        interactionEvent = validated_data.get('interactionEvent', None)

        # create a new user here

        data = validated_data.pop('data', None)

        id = data.get('id')
        name = data.get('name')
        avatar = data.get('avatar')
        username = data.get('username')
        custom_data = data.get('customData')
        identities = data.get('identities')
        is_suspended = data.get('isSuspended')
        primary_email = data.get('primaryEmail')
        primary_phone = data.get('primaryPhone')
        application_id = data.get('applicationId')

        username = username if username else primary_email

        created_at = convert_timestamp_to_date_time(data.get('createdAt'))
        last_sign_in_at = convert_timestamp_to_date_time(data.get('lastSignInAt'))

        other_information = {
            'ip': ip,
            'event': event,
            'hookId': hookId,
            'sessionId': sessionId,
            'userAgent': userAgent,
            'application': application,
            'applicationId': application_id,
            'interactionEvent': interactionEvent,
            'createdAt': created_at.strftime('%Y-%m-%d %H:%M:%s'),
            'customData': custom_data,
            'identities': identities,
        }

        user = User.objects.create(
            sub=id, name=name, email=primary_email, username=username,
            profile_picture_url=avatar, created_at=created_at, last_login=last_sign_in_at,
            is_suspended=is_suspended, mobile_number=primary_phone,
            other_information=other_information, is_customer=True
        )
        return user





