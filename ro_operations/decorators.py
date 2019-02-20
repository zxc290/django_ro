import json
from rest_framework.response import Response
from rest_framework import status
from .tokens import verify_token


def token_required(func):
    def wrapper(instance, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        user_auth = verify_token(token)
        if user_auth is None:
            message = 'token验证过期，请重新登陆'
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        return func(instance, request, *args, **kwargs)
    return wrapper
