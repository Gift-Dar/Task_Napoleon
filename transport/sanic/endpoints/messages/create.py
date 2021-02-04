from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserConflictException

from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException, DBUserNotExistsException
from helpers.auth import check_exist_user


class CreateMessageEndpoint(BaseEndpoint):

    @check_exist_user
    async def method_post(self, request: Request, body: dict, session, token, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)
        sender_id = token.get('uid')
        try:
            db_message = message_queries.create_message(session, request_model, sender_id)
        except DBUserNotExistsException:
            raise SanicUserConflictException('Recipient not found.')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)
