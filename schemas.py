from marshmallow import Schema, validates, fields, ValidationError
import db


def notEmpty(value):
    if not db.messages:
        raise ValidationError("Content can't be empty.")


class MessageSchema(Schema):
    content = fields.String(required=True, validate=notEmpty)
    id = fields.UUID(required=True)

