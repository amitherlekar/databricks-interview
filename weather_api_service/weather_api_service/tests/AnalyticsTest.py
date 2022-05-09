
import unittest
import requests
from Config import LOGIN_URL, LIST_CITIES_URL, WEATHER_FORCAST_URL
import json


class AnalyticsTest(unittest.TestCase):

    LOGIN_USER_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJvbWFyYTEiLCJmaXJzdF9uYW1lIjoiS3JveSBPJ01hcmEiLCJyb2xlIjoidXNlciJ9.rDFqf-k9aPpg4EOoA3uff2Fdh2AoCR5wLtkoUKpBwKI'

    LOGIN_DATA = {
        "user_name": "amit",
        "password": "amit123"
    }
    ADMIN_AUTH_HEADER = {}

    def setUp(self) -> None:
        response = requests.post(url=LOGIN_URL, json=AnalyticsTest.LOGIN_DATA)
        json_response = json.loads(response.content)
        AnalyticsTest.ADMIN_AUTH_HEADER['Authorization'] = json_response["data"]['access_token']
        response = requests.get(url=WEATHER_FORCAST_URL, json=AnalyticsTest.LOGIN_DATA, headers={"Authorization": AnalyticsTest.LOGIN_USER_ACCESS_TOKEN})

    def test_list_cities(self):
        country = "india"
        url = LIST_CITIES_URL.format(country)
        response = requests.get(url=url, headers=AnalyticsTest.ADMIN_AUTH_HEADER)
        self.assertEqual(403, response.status_code)
