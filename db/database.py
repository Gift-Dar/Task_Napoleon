from typing import List

from sqlalchemy import or_, and_, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session, Query

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBUser, DBMessage


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def users(self) -> Query:
        return self.query(DBUser).filter(DBUser.is_delete == False)

    def messages_sender(self) -> Query:
        return self.query(DBMessage).filter(DBMessage.is_delete_sender == False)

    def messages_recipient(self) -> Query:
        return self.query(DBMessage).filter(DBMessage.is_delete_recipient == False)

    def deleted_messages_recipient(self) -> Query:
        return self.query(DBMessage).filter(DBMessage.is_delete_recipient == True)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_user_by_login(self, login: str, add_filter: str = None) -> DBUser:
        query = self.query(DBUser).filter(DBUser.login == login)

        if add_filter is not None:
            query = query.filter(text(add_filter))

        user = query.first()

        return user

    def get_user_by_id(self, uid: int) -> DBUser:
        return self.users().filter(DBUser.id == uid).first()

    def get_message_by_id(self, mid: int) -> DBMessage:
        return self.query(DBMessage).filter(DBMessage.id == mid).first()

    def get_all_deleted_messages(self, uid: int) -> List['DBMessage']:
        return self.query(DBMessage).filter(or_(
            and_(DBMessage.is_delete_sender == True, DBMessage.sender_id == uid),
            and_(DBMessage.is_delete_recipient == True, DBMessage.recipient_id == uid))).all()

    def get_messages_all_inbox(self, uid: int) -> List[DBMessage]:
        return self.messages_recipient().filter(DBMessage.recipient_id == uid).all()

    def get_messages_all_sent(self, uid: int) -> List[DBMessage]:
        return self.messages_sender().filter(DBMessage.sender_id == uid).all()

    def get_recipient_by_mid(self, mid: int) -> DBMessage:
        return self.messages_recipient().filter(DBMessage.id == mid).first()

    def get_sender_by_mid(self, mid: int) -> DBMessage:
        return self.messages_sender().filter(DBMessage.id == mid).first()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)
