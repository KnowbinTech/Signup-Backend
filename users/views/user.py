from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated

from setup.permissions import IsSuperUser
from users.models import User

from users.serializers import UserDataModelSerializer
from users.serializers import ProfileUpdateSerializer
from users.serializers import ResetPassword


from users.utils import get_userdata
from users.filters import UserFilter
from django.conf import settings
from django.core.mail import send_mail


@extend_schema(tags=["Account"])
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Me(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
            Refresh session API

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """

        user = request.user

        if user.is_authenticated:
            return Response({
                'loggedIn': True,
                'user': get_userdata(user)
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                'loggedIn': False,
            }, status=status.HTTP_200_OK)


@extend_schema(tags=["Account"])
class CustomerViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsSuperUser)
    queryset = User.objects.filter(deleted=False, is_customer=True)
    serializer_class = UserDataModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'username']
    filterset_class = UserFilter


@extend_schema(tags=["Account"])
class ProfileUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUpdateSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = self.serializer_class(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully updated your profile..!',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@extend_schema(tags=["Account"])
class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
            Change Password API

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                old_password (char): The old password of the user.
                new_password (char): The new password of the user.
                confirm_password (char): The new password of the user [Retyped].

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        serializer = ResetPassword(data=request.data)

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data['confirm_password']
            serializer.save(password=password)
            return Response({
                'success': True,
                'message': 'Successfully Password Updated'
            }, status=status.HTTP_200_OK)


class SubscribeToSignup(APIView):

    def post(self, request, *args, **kwargs):
        subject = 'Welcome to SIGN UP Casuals'
        message = 'You have subscribed to SIGN UP Casuals'
        email_from = settings.EMAIL_HOST_USER
        email = ['sanjayskumar200@gmail.com']

        send_mail(subject, message, email_from, email)

        return Response('Success')

