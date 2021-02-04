from marshmallow import Schema, fields

from api.base import RequestDto


class RequestRecoveryMessageDtoSchema(Schema):
    is_deleted = fields.Boolean(required=True, default=True)


class RequestRecoveryMessageDto(RequestDto, RequestRecoveryMessageDtoSchema):
    __schema__ = RequestRecoveryMessageDtoSchema
