from core.loggers import logger
from django.conf import settings
import json


JSON_TYPE = 'application/json'


class RequestResponseLoggingMiddleWare:
    """
    Logs all the requests and responses from the application
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _log_request(self, request):
        try:
            request_body = request.body

            if request.headers.get('Content-Type') == JSON_TYPE:
                request_body = json.loads(request_body)
        except Exception:
            request_body = None

        if request_body:
            logger.info(f"Method: {request.method}\nBody: {request_body}")
        else:
            logger.info(f"Method: {request.method}")

        return None

    def _log_response(self, response):
        if hasattr(response, 'data'):
            logger.info(f"Status Code: {response.status_code}\nResponse: {response.data}")
        else:
            logger.info(f"Status Code: {response.status_code}")

        return None

    def __call__(self, request):
        """
        Code to be executed on every request/response call.
        """

        if settings.LOG_REQUEST:
            self._log_request(request)

        response = self.get_response(request)

        if settings.LOG_RESPONSE:
            self._log_response(response)

        return response
