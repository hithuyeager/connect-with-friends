#-------------------------USER ERRORS--------------------------------------------------
class UsersErrors(Exception):
    def __init__(self,message: str,status_code: str):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class InvalidTokenTypeError(UsersErrors):
    def __init__(self):
        super().__init__("INVALID TOKEN TYPE",401)
class TokenExpiredError(UsersErrors):
    def __init__(self):
        super().__init__("TOKEN IS EXPIRED",401)
class InvalidTokenError(UsersErrors):
    def __init__(self):
        super().__init__("INVALID TOKEN",401)
class GoogleTokenExpiredError(UsersErrors):
    def __init__(self):
        super().__init__("GOOGLE TOKEN IS EXPIRED",401)
class GoogleTokenError(UsersErrors):
    def __init__(self):
        super().__init__('SOMETHING WENT WRONG AT GOOGLE',401)
class GoogleLoginError(UsersErrors):
    def __init__(self):
        super().__init__("INAPPROPRIATE LOGIN",403)

