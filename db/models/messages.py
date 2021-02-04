from sqlalchemy import Column, Integer, TEXT, BOOLEAN

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    message = Column(TEXT)
    is_delete_sender = Column(BOOLEAN(), nullable=False, default=False)
    is_delete_recipient = Column(BOOLEAN(), nullable=False, default=False)