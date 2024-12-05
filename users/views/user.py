from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated

from setup.permissions import IsSuperUser
from users.models import User

from users.serializers import UserDataModelSerializer
from users.serializers import ProfileUpdateSerializer

from users.utils import get_userdata

from django.conf import settings
from django.core.mail import send_mail


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


class CustomerViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsSuperUser)
    queryset = User.objects.filter(deleted=False, is_customer=True)
    serializer_class = UserDataModelSerializer


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


class SubscribeToSignup(APIView):

    def post(self, request, *args, **kwargs):
        subject = 'Welcome to SIGN UP Casuals'
        message = 'You have subscribed to SIGN UP Casuals'
        email_from = settings.EMAIL_HOST_USER
        email = ['sanjayskumar200@gmail.com']

        send_mail(subject, message, email_from, email)

        return Response('Success')
