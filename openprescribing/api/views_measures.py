from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

import view_utils as utils
import queries_measures as queries


class MissingParameter(APIException):
    status_code = 400
    default_detail = 'You are missing a required parameter.'


@api_view(['GET'])
def measure_global(request, format=None):
    measure = request.query_params.get('measure', None)
    d = queries.measure_global(measure)
    return Response(d)


@api_view(['GET'])
def measure_by_ccg(request, format=None):
    measure = request.query_params.get('measure', None)
    orgs = utils.param_to_list(request.query_params.get('org', []))
    d = queries.measure_by_ccg(orgs, measure)
    return Response(d)


@api_view(['GET'])
def measure_by_practice(request, format=None):
    measure = request.query_params.get('measure', None)
    orgs = utils.param_to_list(request.query_params.get('org', []))
    if not orgs:
        raise MissingParameter
    d = queries.measure_by_practice(orgs, measure)
    return Response(d)
