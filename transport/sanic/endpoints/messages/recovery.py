from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestRecoveryMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import (
    DBMessageNotExistsException,
    DBIntegrityException,
    DBDataException
)
from db.queries import message as messages_queries
from helpers.auth import check_exist_user
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException


class RecoveryMessageEndpoint(BaseEndpoint):

    @check_exist_user
    async def method_patch(
            self, request: Request, body: dict, session: DBSession, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        rights_holders = [
            messages_queries.get_sender_deleted_message(session, mid),
            messages_queries.get_recipient_deleted_message(session, mid)
        ]
        request_model = RequestRecoveryMessageDto(body)

        if rights_holders is None or token.get('uid') not in rights_holders:
            return await self.make_response_json(status=403)
        elif token.get('uid') == rights_holders[0]:
            try:
                messages_queries.get_message(session, message_id=mid)
                message = messages_queries.recovery_message(
                    session,
                    mid,
                    request_model,
                    attribute='is_delete_sender'
                )
            except DBMessageNotExistsException:
                raise SanicMessageNotFound('Message not found')
        else:
            try:
                messages_queries.get_message(session, message_id=mid)
                message = messages_queries.recovery_message(
                    session,
                    mid,
                    request_model,
                    attribute='is_delete_recipient'
                )
            except DBMessageNotExistsException:
                raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())