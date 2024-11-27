from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth


class LOGTOManagementAPI:
    APP_ID = settings.LOGTO_APP_ID
    APP_SECRET = settings.LOGTO_APP_SECRET
    TOKEN_URL = settings.LOGTO_TOKEN_URL
    MANAGEMENT_ENDPOINT = settings.LOGTO_MANAGEMENT_ENDPOINT
    M2M_RESOURCE = settings.LOGTO_M2M_RESOURCE

    def get_access_token(self):
        auth = HTTPBasicAuth(self.APP_ID, self.APP_SECRET)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "resource": self.M2M_RESOURCE,
            "scope": "all",
        }
        response = requests.post(self.TOKEN_URL, auth=auth, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def __init__(self):
        auth_token = self.get_access_token().get("access_token")
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

    def user_has_password(self, sub):
        """
            API to check if user has password.
        """
        url = f"{self.MANAGEMENT_ENDPOINT}/users/{sub}/has-password"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def check_password(self, sub, password):
        """
            API to verify user password.
        """
        url = f"{self.MANAGEMENT_ENDPOINT}/users/{sub}/password/verify"
        response = requests.post(url, headers=self.headers, json={"password": password})
        response.raise_for_status()
        return response.json()

    def change_password(self, sub, password):
        """
            API to change user password.
        """
        url = f"{self.MANAGEMENT_ENDPOINT}/users/{sub}/password"
        response = requests.patch(url, headers=self.headers, json={"password": password})
        response.raise_for_status()
        return response.json()


