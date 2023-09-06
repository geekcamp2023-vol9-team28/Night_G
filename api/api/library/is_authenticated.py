from typing import Optional

from fastapi import Depends, Header, HTTPException
from jose import ExpiredSignatureError, JWTError, jwt

from api.db.dao.user_dao import UserDAO
from api.settings import settings
from api.web.api.users.schema import UserModelDTO


async def is_authenticated(
    authorization: Optional[str] = Header(default=None),
    user_dao: UserDAO = Depends(),
) -> UserModelDTO:
    """Autheticates a user based on the provided authorization token.

    This function validates the provided authorization token by decofing it
    and verifying its autheticity. If the token is valid, it retrieves the
    associated user information from the database and returns it as a
    UserModelDTO object.

    :param authorization:
        The authorization token provided in the HTTP headers.
        It should be in the format "Bearer <token>".
    :param user_dao: UserDAO object
    :returns: UserModelDTO object
    :raises HTTPException:
        - 400 (Bad Request): If the authorization header is missing.
        - 401 (Unauthorized): If the token is expired or invalid.
        - 404 (Not Found): If the user associated with the token is not found.
    """
    if authorization is None:
        raise HTTPException(
            status_code=400,
            detail="Authorization header is missing.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_request"'},
        )

    jwt_token = authorization.rsplit(maxsplit=1)[-1]

    try:
        payload = jwt.decode(
            jwt_token,
            settings.token_secret_key,
            algorithms=[settings.token_algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    user = await user_dao.get_user(payload["user_id"])

    if user is not None:
        return UserModelDTO.model_validate(user)

    raise HTTPException(
        status_code=404,
        detail="Not found user.",
        headers={"WWW-Authenticate": 'Bearer error="not_found_user"'},
    )