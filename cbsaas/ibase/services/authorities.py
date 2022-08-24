"""Base for all auth to be shared"""
from functools import wraps
from rest_framework.response import Response
from rest_framework.status import ( HTTP_400_BAD_REQUEST,)
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)


def has_view_rights(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        # auth_key = request.headers.get('Authorization', None)
        # client_ref = request.headers.get('client_ref', None)
        # auth = get_authorization_header(request).split()
        # print('gggggggggggggggggggggggjjjjjjjjjjjjjjjjjjjjjjjjj')
        # print(auth[1])
        # if not auth_key or not client_ref:
        #     return Response({'message': 'Auth key or client ref missing'}, status=HTTP_400_BAD_REQUEST)
        # else:
            return function(request, *args, **kwargs)
    return wrap