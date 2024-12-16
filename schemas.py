from marshmallow import Schema, fields, ValidationError
import db
import users_db


def not_empty(value):
    if not db.messages:
        raise ValidationError("Database can't be empty.")


def not_user_empty(value):
    if not users_db.users:
        raise ValidationError("Database can't be empty")
    

def validate_message(value):
    if not value:
        raise ValidationError("No content found in data.")


def find_id(value):
    if not str(value) and str(value) not in db.messages:
        raise ValidationError("Id not in the database.")


def validate_username(value):
    if not value or len(value) < 6 or " " in value or value in users_db.users:
        raise ValidationError("Username incorrect")

def validate_username_logs(value):
    if not value or len(value) < 6 or " " in value or not value in users_db.users:
        raise ValidationError("Username incorrect")

def validate_password(value):
    if not value or not (len(value) >= 8 and ' ' not in value and any(c.isalpha() for c in value) and any(
            c.isdigit() for c in value)):
        raise ValidationError("Password incorrect")


class SendMessageSchema(Schema):
    content = fields.String(required=True, validate=validate_message)


class MessageSchema(Schema):
    content = fields.String(required=True, validate=not_empty)


class ModifyMessageSchema(Schema):
    content = fields.String(required=True, validate=validate_message)
    message_id = fields.UUID(required=True, validate=find_id)


class DeleteMessageSchema(Schema):
    message_id = fields.UUID(required=True, validate=find_id)


class RegisterSchema(Schema):
    username = fields.String(required=True, validate=validate_username)
    password = fields.String(required=True, validate=validate_password)


class UserSchema(Schema):
    content = fields.String(required=True, validate=not_user_empty)


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate_username_logs)
    password = fields.String(required=True, validate=validate_password)


class LogoutSchema(Schema):
    username = fields.String(required=True, validate=validate_username_logs)
    password = fields.String(required=True, validate=validate_password)


