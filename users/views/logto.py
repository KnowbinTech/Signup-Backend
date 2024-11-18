from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

from users.serializers import NewUserSerializer


class LogtoUserCreateHooks(APIView):
    """
        API for saving newly created user
    """
    # Use SessionAuthentication for storing user data in the session cookie.
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = NewUserSerializer

    def post(self, request, *args, **kwargs):
        """
        API for logging user creation hooks

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A response with status code 200.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Save the user to the database
        return Response(status=status.HTTP_200_OK)



