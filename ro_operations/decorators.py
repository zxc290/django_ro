import json
from rest_framework.response import Response
from .tokens import verify_token


def token_required(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        user_auth = verify_token(token)
        if user_auth is None:
            message = 'token验证失败'
            return Response({'code': 2, 'message': message})
        return func(request, *args, **kwargs)
    return wrapper
