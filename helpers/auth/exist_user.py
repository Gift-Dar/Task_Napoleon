from functools import wraps

from db.queries import user as user_queries
from db.exceptions import DBUserNotExistsException
from transport.sanic.exceptions import SanicAuthException


def check_exist_user(view_func):
    @wraps(view_func)
    def wrapper(self, request, body: dict, session, token, *args, **kwargs):
        try:
            user_id = token.get('uid')
            user_queries.get_user(session=session, user_id=user_id)
        except DBUserNotExistsException:
            raise SanicAuthException(message='Unauthorized')
        return view_func(self, request=request, body=body, session=session, token=token, *args, **kwargs)
    return wrapper
