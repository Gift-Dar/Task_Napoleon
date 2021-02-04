from typing import List

from api.request import RequestCreateMessageDto, RequestPatchMessageDto, RequestRecoveryMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, uid: int) -> DBMessage:
    recipient = session.get_user_by_login(login=message.recipient, add_filter='users.is_delete = False')

    if recipient is None:
        raise DBUserNotExistsException

    new_message = DBMessage(
        sender_id=uid,
        message=message.message,
        recipient_id=recipient.id,
    )

    session.add_model(new_message)

    return new_message


def get_message(session: DBSession, message_id: int = None) -> DBMessage:
    db_message = None

    if message_id is not None:
        db_message = session.get_message_by_id(message_id)
    if db_message is None:
        raise DBMessageNotExistsException
    return db_message


def get_all_messages(session: DBSession, uid: int) -> List['DBMessage']:
    list_messages = session.get_messages_all_inbox(uid) + session.get_messages_all_sent(uid)
    list_messages.sort(key=lambda x: x.created_at)
    return list_messages


def get_all_deleted_messages(session, uid: int) -> List['DBMessage']:
    return session.get_all_deleted_messages(uid)


def get_inbox_messages(session: DBSession, uid: int) -> List['DBMessage']:
    list_inbox_messages = session.get_messages_all_inbox(uid)
    list_inbox_messages.sort(key=lambda x: x.created_at)
    return list_inbox_messages


def get_sender(session: DBSession, mid: int):
    message = session.get_sender_by_mid(mid)
    id = None
    if message:
        id = message.sender_id
    return id


def get_sender_deleted_message(session: DBSession, mid: int):
    message = session.get_message_by_id(mid)
    id = None
    if message and message.is_delete_sender == True:
        id = message.sender_id
    return id


def get_recipient_deleted_message(session: DBSession, mid: int):
    message = session.get_message_by_id(mid)
    id = None
    if message and message.is_delete_recipient == True:
        id = message.recipient_id
    return id


def get_recipient(session: DBSession, mid: int):
    message = session.get_recipient_by_mid(mid)
    id = None
    if message:
        id = message.recipient_id
    return id


def get_sent_messages(session: DBSession, uid: int) -> List['DBMessage']:
    list_sent_messages = session.get_messages_all_sent(uid)
    list_sent_messages.sort(key=lambda x: x.created_at)
    return list_sent_messages


def patch_message(session: DBSession, message: RequestPatchMessageDto, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)

    if message.message:
        value = getattr(message, 'message')
        setattr(db_message, 'message', value)

    return db_message


def recovery_message(
        session: DBSession, message_id: int, message: RequestRecoveryMessageDto, attribute='is_delete_sender'
) \
        -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    value = getattr(message, 'is_deleted')
    setattr(db_message, attribute, value)
    return db_message


def delete_message(session: DBSession, message_id: int, attribute='is_delete_sender') -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    value = True
    setattr(db_message, attribute, value)
    return db_message
