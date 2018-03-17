from rest_framework.exceptions import APIException
from rest_framework.views import (
    exception_handler as base_exception_handler,
)


def exception_handler(exc, context):
    response = base_exception_handler(exc, context)

    if response is not None and isinstance(exc, APIException) and isinstance(response.data, dict):
        response.data['codes'] = exc.get_codes()

    return response
