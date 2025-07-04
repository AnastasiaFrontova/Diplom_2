class ResponseText:  # Тексты ответов сервера
    CREATE_USER_DOUBLE = "User already exists"
    REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
    INTERNAL_SERVER_ERROR = 'Internal Server Error'
    NOT_AUTHORIZED = 'You should be authorised'
    INCORRECT_CREDENTIALS = 'email or password are incorrect'
    MISSING_INGREDIENTS = "Ingredient ids must be provided"

class StatusCode:  # Статус-коды ответа сервера
    OK = 200
    BAD_REQUEST = 400
    CREATED = 201
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500