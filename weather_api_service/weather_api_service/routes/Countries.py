from flask import Blueprint, request, make_response
from weather_api_service import getResponseHeaders
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.countryutil import load_countries_into_list, load_countries_json_data
import json
from weather_api_service.services.User import restrict_access

app_countries = Blueprint('app_countries', __name__)

"""
This app exposes API for listing countries and cities from the JSON file.
"""


@app_countries.route('/countries', methods=['GET'])
@restrict_access(role="user")
def get_countries():
    """
        Gets the list of countries
        :return: the API response containing the list of countries
        """
    countries = load_countries_into_list()
    try:
        response = {"countries": countries}
        return make_response(json.dumps(response), 200, getResponseHeaders())
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occurred - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())


@app_countries.route('/cities', methods=['GET'])
@restrict_access(role="user")
def get_cities_of_country():
    """
    Gets the list of cities for a given country
    :return: the API response containing the list of cities
    """
    countries = load_countries_into_list()
    query_params = request.args
    given_country = query_params.get('country')
    response = {"cities": []}

    if given_country is None or len(given_country) == 0 or given_country not in countries:
        return make_response(json.dumps(response), 200, getResponseHeaders())

    try:
        countries_to_json_data = load_countries_json_data()
        cities = []
        for each_country_data in countries_to_json_data:
            country_name = each_country_data['country']
            if country_name.lower() == given_country.lower():
                cities.append(each_country_data['name'])
            response["cities"] = cities
        return make_response(json.dumps(response), 200, getResponseHeaders())

    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occurred - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())
