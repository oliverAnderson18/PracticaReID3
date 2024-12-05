from marshmallow import Schema, validates, fields, ValidationError
from flask import request
import db


def not_empty(value):
    if not db.messages:
        raise ValidationError("Database can't be empty.")


def validate_message(value):
    data = request.json
    if not data or "content" not in data:
        raise ValidationError("No content found in data.")


def find_id(message_id):
    if message_id not in db.messages:
        raise ValidationError("Id not in the database.")


class MessageSchema(Schema):
    content = fields.String(required=True, validate=not_empty)
    id = fields.UUID(required=True)


class SendMessageSchema(Schema):
    content = fields.String(required=True, validate=validate_message)


class ModifyMessageSchema(Schema):
    content = fields.String(required=True, validate=validate_message)
    message_id = fields.UUID(required=True, validate=find_id)


class DeleteMessageSchema(Schema):
    id = fields.UUID(required=True, validate=find_id)
