import json


COUNTRIES_JSON_FILE = "./data/country_data.json"
COUNTRIES_JSON_DATA = []
COUNTRY_LIST =[]
CITY_LIST = []

"""
An utility to read country JSON file
"""

def read_country_file():
    """
    Helper function to read the json file which has a list of counties
    :return: the list of JSON objects
    """
    with open(COUNTRIES_JSON_FILE, 'rb') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(e)
            raise
    return data


def load_countries_json_data():
    """
    Loads the list of countries into a global variable
    :return: the list of JSON objects
    """
    global COUNTRIES_JSON_DATA

    if not len(COUNTRIES_JSON_DATA):
        COUNTRIES_JSON_DATA = read_country_file()
    return COUNTRIES_JSON_DATA


def load_countries_into_list():
    """
    Loads the list of countries and save it in a global variable
    :return: the list of countries
    """
    global COUNTRIES_JSON_DATA
    countries_to_json_data = load_countries_json_data();
    if not len(COUNTRY_LIST):
        for each_country_data in countries_to_json_data:
            country_name = each_country_data['country']
            if country_name not in COUNTRY_LIST:
                COUNTRY_LIST.append(country_name)

    return COUNTRY_LIST
