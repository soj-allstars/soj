from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import ObjectDoesNotExist
from django.http.response import JsonResponse
from rest_framework import status
import logging


class SojMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        # caution: this may lead to bugs hard to locate
        if isinstance(exception, MultiValueDictKeyError):
            return JsonResponse({'detail': f'hi, you missed {exception} parameter.'},
                                status=status.HTTP_400_BAD_REQUEST)

        if isinstance(exception, ObjectDoesNotExist):
            return JsonResponse({'detail': f'hi, corresponding {exception} please ensure the *id you passed is correct.'},
                                status=status.HTTP_404_NOT_FOUND)
        logging.error(exception, exc_info=True)
        return JsonResponse({'detail': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
