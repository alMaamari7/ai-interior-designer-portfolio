class AuthError(Exception):
    pass


class EmailAlreadyExistsError(AuthError):
    pass


class PasswordsDoNotMatchError(AuthError):
    pass


class PasswordTooShortError(AuthError):
    pass


class InvalidTokenError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass
