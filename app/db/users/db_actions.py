from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from app.db.users.models import User, get_db
from app.config import settings


def decode_jwt(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/urers/token/"))]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(payload=payload, key=settings.secret_key, algorithm=[settings.algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    return username
    