import json

from flask import Blueprint, request, make_response

from weather_api_service import getResponseHeaders
from weather_api_service.services.AnalyticsUtil import get_topn_records, get_result_in_list, validate_value_of_topn
from weather_api_service.services.AnalyticsUtil import validate_value_of_entity_type
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.services.User import restrict_access

"""
This app exposes APIs for analytics. All APIs are authorised to be consumed by users with admin role only.
"""

app_analytics = Blueprint('app_analytics', __name__)


@app_analytics.route('/analytics/topn', methods=['GET'])
@restrict_access(role="admin")
def get_forecast_of_city():
    query_params = request.args
    topn = query_params.get('n')
    entity_type = query_params.get('type')

    try:
        number = validate_value_of_topn(topn)
        validate_value_of_entity_type(entity_type)
    except ValueError as e:
        response = {"message": str(e)}
        return make_response(json.dumps(response), 400, getResponseHeaders())

    try:
        result_set = get_topn_records(entity_type, number)
        result_list = get_result_in_list(result_set)

        response = {"top_n_records": result_list}
        return make_response(json.dumps(response), 200, getResponseHeaders())
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occurred - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())
