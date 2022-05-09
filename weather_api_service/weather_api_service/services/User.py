from weather_api_service import db, secret_key, encrypt, decrypt
from weather_api_service.models.User import User
from functools import wraps
from flask import request, current_app, abort
import jwt


def validate_user_credentials(user_name: str, password: str) -> (int, str, dict):
    """
    Checks the login attempt by the user. Returns the authentication token if login is successful.
    :param user_name: the user name
    :param password: the password
    :return: the JSON response containing the authentication token
    """
    status = 401
    message = 'Incorrect username or password'
    user = None
    try:
        user_obj = (
            db.session.query(User)
                .filter(User.username == user_name)
                .first()
        )
        if user_obj:
            entered_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            if entered_password_enc == user_obj.password:
                status = 200
                message = 'User successfully authenticated'
                user = {
                    'user_name': user_obj.username,
                    'first_name': user_obj.full_name,
                    'role': user_obj.role
                }
            else:
                message = 'Password is invalid.'
        else:
            message = 'Username is invalid.'
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, user


def get_current_user(auth_token):
    """
    Decodes the authentication token to retrieve the user from the database
    :param auth_token: the authentication token
    :return:
    """
    data = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
    current_user = (
        db.session.query(User)
            .filter(User.username == data['user_name'])
            .first()
    )
    return current_user


def check_credential(request):
    """
    Checks the login attempt by the user who as given the authentication token in the Authorization header
    :param request: the HTTP request object
    :return: the user if login is successful; Unauthorized response on failure.
    """
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
    if not token:
        return {
                   "message": "Authentication token is missing from the request header."
               }, 401
    try:
        current_user = get_current_user(token)
        if current_user is None:
            return {
                       "message": "Authentication token is invalid."
                   }, 401
    except Exception as e:
        return {
                   "message": "Authentication token is invalid."
               }, 401
    return current_user


def restrict_access(role: str, return_user=False):
    """
    Verifies the login attempt and also checks the user role for API access.
    :param role: the required role to access the API
    :param return_user: if True, user object will be returned; false otherwise
    :return: the user object if return_user is True
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = check_credential(request)
            if type(response) is tuple:
                return response

            if not response.role or role.lower() not in response.role.lower():
                return {
                            "message": "You are not authorized to access this resource.",
                       }, 403
            if return_user:
                return func(response, *args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator
