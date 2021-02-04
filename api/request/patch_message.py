from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchMessageDtoSchema(Schema):
    message = fields.Str()


class RequestPatchMessageDto(RequestDto, RequestPatchMessageDtoSchema):
    __schema__ = RequestPatchMessageDtoSchema


