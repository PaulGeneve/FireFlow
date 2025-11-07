from marshmallow import Schema, fields


class ErrorSchema(Schema):
    code = fields.Int()
    status = fields.Str()
    message = fields.Str()


class Error400Schema(ErrorSchema):
    code = fields.Int(metadata={'example': 400})
    status = fields.Str(metadata={'example': 'Bad Request'})
    message = fields.Str(metadata={'example': 'Invalid parameter'})


class Error404Schema(ErrorSchema):
    code = fields.Int(metadata={'example': 404})
    status = fields.Str(metadata={'example': 'Not Found'})
    message = fields.Str(metadata={'example': 'Resource not found'})


class Error409Schema(ErrorSchema):
    code = fields.Int(metadata={'example': 409})
    status = fields.Str(metadata={'example': 'Conflict'})
    message = fields.Str(metadata={'example': 'Resource already exists'})


class Error401Schema(ErrorSchema):
    code = fields.Int(metadata={'example': 401})
    status = fields.Str(metadata={'example': 'Unauthorized'})
    message = fields.Str(metadata={'example': 'Missing or invalid token'})


class Error403Schema(ErrorSchema):
    code = fields.Int(metadata={'example': 403})
    status = fields.Str(metadata={'example': 'Forbidden'})
    message = fields.Str(metadata={'example': 'Insufficient permissions'})