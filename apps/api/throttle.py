from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle, UserRateThrottle
from rest_framework.views import APIView

# class RandomRateThrottle(BaseThrottle):
#     throttle_scope = 'uploads'
#     scope = 'test'
#     def allow_request(self, request, view):
#         return random.randint(1, 10) != 1
