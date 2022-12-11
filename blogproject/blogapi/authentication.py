from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import BlogUser


import datetime
import jwt
from django.conf import settings





class SafeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise exceptions.AuthenticationFailed({"status": False, "data": 'access_token not provided'})
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({"status": False, "data": 'access_token expired'})

        except IndexError:
            raise exceptions.AuthenticationFailed({"status": False, "data": 'Token prefix missing'})

        user = BlogUser.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed({"status": False, "data": 'User not found'})

        if not user.is_active:
            raise exceptions.AuthenticationFailed({"status": False, "data": 'User is not active'})

        return user, None


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.JWT_SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.JWT_REFRESH_TOKEN_SECRET, algorithm='HS256')

    return refresh_token
