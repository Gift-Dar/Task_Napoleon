from sqlalchemy import Column, VARCHAR, BOOLEAN, LargeBinary

from db.models import BaseModel


class DBUser(BaseModel):

    __tablename__ = 'users'

    login = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(LargeBinary(), nullable=False)
    first_name = Column(VARCHAR(50), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    is_delete = Column(BOOLEAN(), nullable=False, default=False)

