import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jose import jwt
import requests
from django.conf import settings
from users.models import User


class LogtoJWTAuthentication(JWTAuthentication):
    def __init__(self):
        self.jwks_url = settings.LOGTO_CERTS_URL  # Replace with your Logto JWKS URL
        self.issuer = settings.LOGTO_ISSUER  # Replace with your Logto issuer URL
        self.audience = settings.LOGTO_AUDIENCE  # Replace with your Logto issuer URL
        jwks = requests.get(self.jwks_url)
        self.jwks = jwks.json()
        super().__init__()

    def decode_token(self, token):
        alg = jwt.get_unverified_header(token).get('alg')

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
            print('Exception : ', e)
            raise AuthenticationFailed('Invalid token')

    def authenticate(self, request):
        header = self.get_header(request)
        try:
            raw_token = self.get_raw_token(header)
        except Exception as e:
            print('Exception : ', e)
            raise AuthenticationFailed('Invalid token')

        if raw_token is None:
            return None

        # Decode and verify token
        validated_token = self.decode_token(raw_token)

        return self.find_user(validated_token), validated_token

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



