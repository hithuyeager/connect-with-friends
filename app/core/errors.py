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
class WrongPasswordError(UsersErrors):
    def __init__(self):
        super().__init__("WRONG PASSWORD",401)
class InvalidHashError(UsersErrors):
    def __init__(self):
        super().__init__("PLEASE PROVIDE PROPER HASH",401)
class HashingError(UsersErrors):
    def __init__(self):
        super().__init__("ERROR WHILE HASHING PASSSWORD",501)
class EmailAlreadyExistError(UsersErrors):
    def __init__(self):
        super().__init__("EMAIL ALREADY EXIST",401)
class UsernameExistError(UsersErrors):
    def __init__(self):
        super().__init__("USERNAME ALREADY TAKEN",401)
class GoogleUserError(UsersErrors):
    def __init__(self):
        super().__init__("EMAIL SIGNEDUP WITH GOOGLE",401)
class EmailNotExistError(UsersErrors):
    def __init__(self):
        super().__init__("EMAIL DIDNT SIGNED UP",401)
class InvalidPasswordError(UsersErrors):
    def __init__(self):
        super().__init__("INCORRECT PASSWORD",401)
class NoUsersMatchError(UsersErrors):
    def __init__(self):
        super().__init__("NO USER MATCHED",400)
class InvalidSession(UsersErrors):
    def __init__(self):
        super().__init__("THIS SESSION HAS EXPIRED",403)
class FraudDetection(UsersErrors):
    def __init__(self):
        super().__init__("UNKNOWN REFRESH TOKEN USED",400)


        
