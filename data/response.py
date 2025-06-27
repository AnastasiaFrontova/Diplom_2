class ResponseText:  # Тексты ответов сервера
    CREATE_USER_DOUBLE = "User already exists"
    INTERNAL_SERVER_ERROR = 'Internal Server Error'
    RESPONSE_NOT_AUTHORIZED = 'You should be authorised'


class StatusCode:  # Статус-коды ответа сервера
    OK = 200
    BAD_REQUEST = 400
    CREATED = 201
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500