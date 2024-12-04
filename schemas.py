from marshmallow import Schema, validates, fields, ValidationError
import db


def notEmpty(content):
    if not content:
        raise ValidationError({"Error": "Content not found"})


class MessageSchema(Schema):
    content = fields.String(validate=notEmpty(db.messages))
