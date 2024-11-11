from rest_framework.views import exception_handler

KEY_WRAPPER = 'errors'


def exception_handler_wrapper(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 400 and KEY_WRAPPER not in response.data:
        errors = response.data
        response.data = {}
        response.data[KEY_WRAPPER] = errors

    return response
