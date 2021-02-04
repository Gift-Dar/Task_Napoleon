import pytest

from helpers.auth.exist_user import check_exist_user
from transport.sanic.base import SanicEndpoint
from transport.sanic.exceptions import SanicAuthException


@pytest.mark.asyncio
async def test_check_exist_user(request_factory, patched_context, token_data, mocker):
    patched_query = mocker.patch('db.queries.user.get_user')
    patched_query.return_value = None
    request = request_factory(method='get')
    endpoint = SanicEndpoint(None, patched_context, '', ())

    decorated_func = check_exist_user(endpoint)
    response = decorated_func(request, token=token_data)
    with pytest.raises(SanicAuthException):
        await decorated_func(request, token=token_data)
