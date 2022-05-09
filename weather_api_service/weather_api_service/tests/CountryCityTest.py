
import unittest
import requests
from Config import LOGIN_URL, LIST_COUNTRIES_URL, LIST_CITIES_URL
import json


class CountryCityTest(unittest.TestCase):

    LOGIN_USER_ACCESS_TOKEN = None

    LOGIN_DATA = {
        "user_name": "adams1",
        "password": "XGoqXnMB"
    }
    USER_AUTH_HEADER = {}


    def setUp(self) -> None:
        response = requests.post(url=LOGIN_URL, json=CountryCityTest.LOGIN_DATA)
        json_response = json.loads(response.content)
        CountryCityTest.LOGIN_USER_ACCESS_TOKEN = json_response["data"]['access_token']
        CountryCityTest.USER_AUTH_HEADER = {'Authorization': CountryCityTest.LOGIN_USER_ACCESS_TOKEN}

    def test_list_cities(self):
        country = "India"
        url = LIST_CITIES_URL.format(country)
        response = requests.get(url=url, headers=CountryCityTest.USER_AUTH_HEADER)
        response_json = json.loads(response.content)
        test = len(response_json['cities']) > 0
        self.assertTrue(test)

    def test_list_countries(self):
        url = LIST_COUNTRIES_URL
        response = requests.get(url=url, headers=CountryCityTest.USER_AUTH_HEADER)
        response_json = json.loads(response.content)
        test = len(response_json['countries']) > 0
        self.assertTrue(test)

    def test_list_cities_with_invalid_city(self):
        country = "Titanic"
        url = LIST_CITIES_URL.format(country)
        response = requests.get(url=url, headers=CountryCityTest.USER_AUTH_HEADER)
        response_json = json.loads(response.content)
        self.assertEqual(0, len(response_json["cities"]), msg=response.content)
