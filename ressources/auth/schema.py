from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    uuid = fields.Str()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    roles = fields.List(fields.String())

class UserArgsSchema(Schema):
    name = fields.String()
    email = fields.String()
    password = fields.String()
    role = fields.String()

class UserLoginSchema(Schema):
    name = fields.String()
    password = fields.String()

class TokenSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()

class UserTokenSchema(Schema):
    message = fields.Str()
    tokens = fields.Nested(TokenSchema)
