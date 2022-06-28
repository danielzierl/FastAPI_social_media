from passlib.context import CryptContext

pdw_context = CryptContext(schemes=["bcrypt"])


def hash(password: str):
    return pdw_context.hash(password)


def verifyPswd(plainPswd, HashedPswd):
    return pdw_context.verify(plainPswd, HashedPswd)
