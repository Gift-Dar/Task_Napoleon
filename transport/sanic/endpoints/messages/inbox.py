from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseMessageDto
from db.database import DBSession
from db.queries import message as message_queries
from helpers.auth import check_exist_user
from transport.sanic.endpoints import BaseEndpoint


class AllInboxMessageEndpoint(BaseEndpoint):

    @check_exist_user
    async def method_get(
            self, request: Request, body: dict, session: DBSession, token, *args, **kwargs
    ) -> BaseHTTPResponse:
        uid = token.get('uid')
        db_messages = message_queries.get_inbox_messages(session, uid)
        response_model = ResponseMessageDto(db_messages, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())