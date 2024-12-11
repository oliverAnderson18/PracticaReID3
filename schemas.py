from marshmallow import Schema, fields, ValidationError
import db


def not_empty(value):
    if not db.messages:
        raise ValidationError("Database can't be empty.")


def validate_message(value):
    if not value:
        raise ValidationError("No content found in data.")


def find_id(value):
    if not str(value) and str(value) not in db.messages:
        raise ValidationError("Id not in the database.")


class SendMessageSchema(Schema):
    content = fields.String(required=True, validate=validate_message)


class MessageSchema(Schema):
    content = fields.String(required=True, validate=not_empty)


class ModifyMessageSchema(Schema):
    content = fields.String(required=True, validate=validate_message)
    message_id = fields.UUID(required=True, validate=find_id)


class DeleteMessageSchema(Schema):
    message_id = fields.UUID(required=True, validate=find_id)

