from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.CreateUserEndpoint(
            config, context, uri='/user', methods=['POST'],
        ),
        endpoints.AuthUserEndpoint(
            config, context, uri='/auth', methods=['POST'],
        ),
        endpoints.UserEndpoint(
            config, context, uri='/user/<uid:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        ),
        endpoints.CreateMessageEndpoint(
            config, context, uri='/msg', methods=['POST'], auth_required=True,
        ),
        endpoints.AllMessageEndpoint(
            config, context, uri='/msg', methods=['GET'], auth_required=True,
        ),
        endpoints.AllInboxMessageEndpoint(
            config, context, uri='/msg/inbox', methods=['GET'], auth_required=True,
        ),
        endpoints.AllSentMessageEndpoint(
            config, context, uri='/msg/sent', methods=['GET'], auth_required=True,
        ),
        endpoints.MessageEndpoint(
            config, context, uri='msg/<mid:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        ),
        endpoints.AllDeletedMessagesEndpoint(
            config, context, uri='msg/trash', methods=['GET'], auth_required=True,
        ),
        endpoints.RecoveryMessageEndpoint(
            config, context, uri='msg/trash/<mid:int>', methods=['PATCH'], auth_required=True,
        ),
    )
