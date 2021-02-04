from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBDataException, DBIntegrityException
from db.queries import message as messages_queries
from helpers.auth import check_exist_user
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException


class MessageEndpoint(BaseEndpoint):

    @check_exist_user
    async def method_get(
            self, request: Request, body: dict, session: DBSession, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        rights_holders = [messages_queries.get_sender(session, mid), messages_queries.get_recipient(session, mid)]

        if rights_holders is None or token.get('uid') not in rights_holders:
            return await self.make_response_json(status=403)

        try:
            message = messages_queries.get_message(session, mid)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())

    @check_exist_user
    async def method_patch(
            self, request: Request, body: dict, session: DBSession, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        right_holder = messages_queries.get_sender(session, mid)

        if right_holder is None or token.get('uid') != right_holder:
            return await self.make_response_json(status=403)

        request_model = RequestPatchMessageDto(body)

        try:
            messages_queries.get_message(session, mid)
            message = messages_queries.patch_message(session, request_model, mid)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())

    @check_exist_user
    async def method_delete(
            self, request: Request, body: dict, session: DBSession, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        rights_holders = [messages_queries.get_sender(session, mid), messages_queries.get_recipient(session, mid)]
        if rights_holders is None or token.get('uid') not in rights_holders:
            return await self.make_response_json(status=403)
        elif token.get('uid') == rights_holders[0]:
            try:
                messages_queries.get_message(session, message_id=mid)
                message = messages_queries.delete_message(session, mid)
            except DBMessageNotExistsException:
                raise SanicMessageNotFound('Message not found')
        else:
            try:
                messages_queries.get_message(session, message_id=mid)
                message = messages_queries.delete_message(session, mid, attribute='is_delete_recipient')
            except DBMessageNotExistsException:
                raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
