import json
import requests

from flask import Blueprint, request, make_response

from weather_api_service import getResponseHeaders
from weather_api_service import weather_api_key, db
from weather_api_service.countryutil import load_countries_json_data
from weather_api_service.models.AuditLog import AuditCountry, AuditCity, AuditUser
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.services.User import restrict_access
from datetime import datetime

"""
This app consumes APIs from weatherapi.com
"""

app_weather = Blueprint('app_weather', __name__)

WEATHER_FORECAST_URI = 'http://api.weatherapi.com/v1/forecast.json'


def get_weather_forecast(city, days):
    """
    Invokes forecast API on weatherapi.com for the given city and number of days
    :param city: The name of the city
    :param days: The number of days in the future for get weather forecast
    :return: the API response object
    """
    query_params = {
        'key': weather_api_key,
        'q': city
    }

    if days is not None and int(days) > 0:
        query_params['days'] = int(days)
    response = requests.get(WEATHER_FORECAST_URI, params=query_params)
    return response


@app_weather.route('/weather/forecast', methods=['GET'])
@restrict_access(role="user", return_user=True)
def get_forecast_of_city(current_user):
    """
    Gets the weather forecast of given city
    :param current_user: the logged-in user
    :return:  the API response
    """
    query_params = request.args
    given_city = query_params.get('city')
    days = query_params.get('days')

    if given_city is None or len(given_city) == 0:
        response = {"message": "Invalid input: city is not given."}
        return make_response(json.dumps(response), 400, getResponseHeaders())

    try:
        countries_to_json_data = load_countries_json_data()
        city_found = False
        for each_country_data in countries_to_json_data:
            city = each_country_data['name']
            if city.lower() == given_city.lower():
                city_found = True
                country_name = each_country_data['country']
                break

        if not city_found:
            response = {"message": "Invalid input: Given city is not known: " + given_city}
            return make_response(response, 400, getResponseHeaders())

        response = get_weather_forecast(city, days)
        status_code = response.status_code
        if status_code == 200:
            log_forecast_request(current_user.full_name, country_name, city)

        return make_response(response.content, status_code, getResponseHeaders())

    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occurred - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())


def log_forecast_request(full_name_of_user, country, city):
    """
    Wrapper method to audit the user, country and city used for querying th forcast
    :param full_name_of_user: the name of the user
    :param country: the name of the country
    :param city: the name of the city
    """
    try:
        log_forcast_request_of_city(city)
        log_forcast_request_of_country(country)
        log_forcast_request_of_user(full_name_of_user)
        db.session.commit()
    except Exception as e:
        print(str(e))
        db.session.rollback()


def log_forcast_request_of_country(country):
    """
    Method to audit the country used for querying th forcast
    :param country: the name of the country
    """

    existing_record = (
           db.session.query(AuditCountry)
               .filter(AuditCountry.name == country)
               .first()
    )
    if existing_record:
        existing_record.hits = existing_record.hits + 1
        existing_record.lastUpdateTimestamp = str(datetime.utcnow())
        print(f'Record exists for {existing_record.name}. Total hits: {existing_record.hits}')
        db.session.merge(existing_record)
    else:
        newRecord = AuditCountry()
        newRecord.name = country
        newRecord.hits = 1
        newRecord.lastUpdateTimestamp = str(datetime.utcnow())
        print(f'Adding new record {newRecord.name}. Total hits: {newRecord.hits}')
        db.session.add(newRecord)


def log_forcast_request_of_city(city):
    """
    Method to audit the city used for querying the forcast
    :param city: the name of the city
    """
    existing_record = (
           db.session.query(AuditCity)
               .filter(AuditCity.name == city)
               .first()
    )
    if existing_record:
        existing_record.hits = existing_record.hits + 1
        existing_record.lastUpdateTimestamp = str(datetime.utcnow())
        print(f'Record exists for {existing_record.name}. Total hits: {existing_record.hits}')
        db.session.merge(existing_record)
    else:
        newRecord = AuditCity()
        newRecord.name = city
        newRecord.hits = 1
        newRecord.lastUpdateTimestamp = str(datetime.utcnow())
        print(f'Adding new record {newRecord.name}. Total hits: {newRecord.hits}')
        db.session.add(newRecord)


def log_forcast_request_of_user(username):
    """
    Method to audit the user used for querying th forcast
    :param username: the full name of the user
        """
    existing_record = (
           db.session.query(AuditUser)
               .filter(AuditUser.name == username)
               .first()
    )
    if existing_record:
        existing_record.hits = existing_record.hits + 1
        existing_record.lastUpdateTimestamp = str(datetime.utcnow())
        print(f'Record exists for {existing_record.name}. Total hits: {existing_record.hits}')
        db.session.merge(existing_record)
    else:
        newRecord = AuditUser()
        newRecord.name = username
        newRecord.hits = 1
        newRecord.lastUpdateTimestamp = str(datetime.utcnow())
        print(f'Adding new record {newRecord.name}. Total hits: {newRecord.hits}')
        db.session.add(newRecord)
