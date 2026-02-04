# middleware/timeout_middleware.py

import signal
from django.http import JsonResponse

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Request timed out!")

class TimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(600)  # Set timeout to 10 minutes (600 seconds)
        try:
            response = self.get_response(request)
        except TimeoutException:
            return JsonResponse({"error": "Request timed out"}, status=504)
        finally:
            signal.alarm(0)  # Disable the alarm after request is processed
        return response
