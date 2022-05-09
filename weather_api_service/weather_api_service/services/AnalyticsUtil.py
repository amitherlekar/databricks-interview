from weather_api_service import db
from weather_api_service.models.AuditLog import AuditCountry, AuditCity, AuditUser

ENTITY_TYPES = ["user", "city", "country"]


def validate_value_of_topn(topn):
    """
    Validates the given number
    :param topn: the number of records
    :return: the number in integer form
    :raises ValueError:  when the input is invalid
    """
    number = 0
    try:
        if not topn:
            raise ValueError("The value of top n is not given: " + str(topn))
        number = int(topn)
        if number <= 0:
            raise ValueError("The value of top n is invalid: " + topn)
        return number
    except ValueError as e:
        raise e


def validate_value_of_entity_type(entity_type):
    """
    Validates the entity type.
    :param entity_type: the type. Must be one of ENTITY_TYPES
    """
    if not entity_type or entity_type.lower() not in ENTITY_TYPES:
        raise ValueError("The value of type is invalid: " + str(entity_type))


def get_topn_countries(topn):
    """
    Returns the top most records of AuditTopCountry in descending order of number of hits
    :param topn: the required number representing the top countries
    :return: the result set
    """
    result = (db.session.query(AuditCountry)
             .order_by(AuditCountry.hits.desc()).limit(topn).all())
    return result


def get_topn_cities(topn):
    """
    Returns the top most records of AuditTopCity in descending order of number of hits
    :param topn: the required number representing the top cities
    :return: the result set
    """
    result = (db.session.query(AuditCity)
             .order_by(AuditCity.hits.desc()).limit(topn).all())
    return result


def get_topn_users(topn):
    """
    Returns the top most records of AuditTopUser in descending order of number of hits
    :param topn: the required number representing the top users
    :return: the result set
    """
    result = (db.session.query(AuditUser)
             .order_by(AuditUser.hits.desc()).limit(topn).all())
    return result


def get_topn_records(entity_type, topn):
    """
    The wrapper method to get the top n records in descending order
    :param entity_type: the entity type. Must be one of "city", "country", "user"
    :param topn: the required number representing the top users
    :return: the result set
    """
    match entity_type.strip().lower():
        case "city":
            return get_topn_cities(topn)
        case "country":
            return get_topn_countries(topn)
        case "user":
            return get_topn_users(topn)


def get_result_in_list(result_obj):
    """
    Converts result set into python list
    :param result_obj: the result set
    :return:  the list of dictionaries
    """
    result_list = []
    if result_obj and type(result_obj) is list:
        for item in result_obj:
            result_list.append({"name": item.name, "hits": item.hits, "lastUpdateTimestamp": item.lastUpdateTimestamp})
    return result_list