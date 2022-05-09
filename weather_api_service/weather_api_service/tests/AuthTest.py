
import unittest
import requests
from Config import LOGIN_URL, ADMIN_URL, LIST_COUNTRIES_URL


class AuthTest(unittest.TestCase):

    LOGIN_USER_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJvbWFyYTEiLCJmaXJzdF9uYW1lIjoiS3JveSBPJ01hcmEiLCJyb2xlIjoidXNlciJ9.rDFqf-k9aPpg4EOoA3uff2Fdh2AoCR5wLtkoUKpBwKI'

    def test_successful_login(self):
        login_data = {
            "user_name": "adams1",
            "password": "XGoqXnMB"
        }
        response = requests.post(url=LOGIN_URL, json=login_data)
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_login_bad_request(self):
        login_data = {
            "username": "adams1",
            "password": "XGoqXnMB"
        }
        response = requests.post(url=LOGIN_URL, json=login_data)
        self.assertEqual(400, response.status_code, msg=response.content)

    def test_login_unauthorized_request(self):
        login_data = {
            "user_name": "adams1",
            "password": "XGoqXnMB1"
        }
        response = requests.post(url=LOGIN_URL, json=login_data)
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_login_with_correct_access_token(self):
        login_data = {
            "Authorization": AuthTest.LOGIN_USER_ACCESS_TOKEN
        }
        response = requests.get(url=LIST_COUNTRIES_URL, headers=login_data)
        self.assertEqual(200, response.status_code, msg=response.content)

    def test_login_with_wrong_access_token(self):
        login_data = {
            "Authorization": "SomethingIsFishyHere"
        }
        response = requests.get(url=LIST_COUNTRIES_URL, headers=login_data)
        self.assertEqual(401, response.status_code, msg=response.content)

    def test_unauthorized_login_with_user_access_token(self):
        login_data = {
            "Authorization": AuthTest.LOGIN_USER_ACCESS_TOKEN
        }
        response = requests.get(url=ADMIN_URL, headers=login_data)
        self.assertEqual(403, response.status_code, msg=response.content)


