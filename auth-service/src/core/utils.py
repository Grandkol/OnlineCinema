from core.config import settings
import jwt
import bcrypt
from datetime import datetime, timedelta


async def encode_access_token(
    payload: dict,
    expiry: float,
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in,
                    "iat": datetime.utcnow()})

    encoded = jwt.encode(payload, key=private_key, algorithm=algorithm)

    return encoded


async def encode_refresh_token(
    payload: dict,
    expiry: float,
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in,
                    "iat": datetime.utcnow()}
                   )
    return jwt.encode(payload, key=private_key, algorithm=algorithm)

def decode_access_token(
    token: str | bytes,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):

    # print(public_key)
    # print(algorithm)
    print(f"Public Key: {public_key}")

    decoded = jwt.decode(token, key=public_key, algorithms=algorithm)

    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password=hashed_password)
