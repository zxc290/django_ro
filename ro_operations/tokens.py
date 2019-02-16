import time
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer


def gen_json_web_token(user_info):
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 8 * 60 * 60)
    timestamp = time.time()
    user_info['iat'] = timestamp
    token = s.dumps(user_info)
    return token


def verify_token(token):
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 8 * 60 * 60)
    try:
        user_auth = s.loads(token)
    except:
        return
    if ('user_id' not in user_auth) or ('username' not in user_auth):
        return
    return user_auth