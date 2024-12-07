import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BaseAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.exceptions import AuthenticationFailed
from jose import jwt
import requests
from django.conf import settings
from users.models import User


class NoOpAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None  # Always return None to bypass authentication


class LogtoJWTAuthentication(JWTAuthentication):
    def __init__(self):
        self.jwks_url = settings.LOGTO_CERTS_URL  # Replace with your Logto JWKS URL
        self.issuer = settings.LOGTO_ISSUER  # Replace with your Logto issuer URL
        self.audience = settings.LOGTO_AUDIENCE  # Replace with your Logto issuer URL
        jwks = requests.get(self.jwks_url)
        self.jwks = jwks.json()
        super().__init__()

    def decode_token(self, token):

        try:
            payload = jwt.decode(
                token,
                self.jwks,
                algorithms=jwt.get_unverified_header(token).get('alg'),
                audience=self.audience,  # Replace with the audience
                issuer=self.issuer,
                options={'verify_at_hash': False}
            )
            return payload
        except Exception as e:
            print('-------------------------------')
            print('Exception : ', e)
            print('-------------------------------')
            raise AuthenticationFailed('Invalid token')

    def authenticate(self, request):
        if not request.headers.get('Authorization'):
            return None

        header = self.get_header(request)
        try:
            raw_token = self.get_raw_token(header)
        except Exception as e:
            print('Exception on getting the raw token')
            return None

        if raw_token is None:
            return None

        try:
            validated_token = self.decode_token(raw_token)
            return self.find_user(validated_token), validated_token
        except Exception as e:
            print('Exception on finding the user', e)
            return None

    def find_user(self, validated_token):
        user_id_claim = settings.SIMPLE_JWT.get('USER_ID_CLAIM')
        user_id_field = settings.SIMPLE_JWT.get('USER_ID_FIELD')

        # Create user and set in context if successful
        user_id = validated_token.get(user_id_claim)

        try:
            user = User.objects.get(**{user_id_field: user_id})
            return user
        except User.DoesNotExist:
            print('calling an e')
            raise AuthenticationFailed('Invalid token')

        except Exception as e:
            print('Exception : ', e)
            raise AuthenticationFailed('Invalid token')


class LogtoJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'users.authentication.LogtoJWTAuthentication'  # The authentication class to associate
    name = "LogtoJWT"  # Name to display in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }



