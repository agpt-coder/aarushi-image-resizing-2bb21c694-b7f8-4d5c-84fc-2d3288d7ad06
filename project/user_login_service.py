from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class UserProfile(BaseModel):
    """
    A simplified user profile model for the login response.
    """

    id: str
    email: str
    role: str
    displayName: str


class UserLoginResponse(BaseModel):
    """
    Provides feedback on the login request, including a session token and user information.
    """

    user: UserProfile
    token: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies whether a plaintext password matches a given hash.

    Args:
    plain_password (str): The plaintext password to verify.
    hashed_password (str): The hashed password to compare against.

    Returns:
    bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new access token with the given data and expiry.

    Args:
    data (dict): The data to encode into the access token.
    expires_delta (Optional[timedelta]): The time after which the token expires.

    Returns:
    str: An encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def user_login(email: str, password: str) -> UserLoginResponse:
    """
    Handles user login requests by verifying user credentials, generating a session token, and returning user information.

    Args:
    email (str): User's email address as registered.
    password (str): User's password for authentication. This should be handled with care and never stored in plain text.

    Returns:
    UserLoginResponse: Provides feedback on the login request, including a session token and user information.

    Raises:
    HTTPException: For invalid credentials with a 401 status code.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    user_profile = UserProfile(
        id=user.id, email=user.email, role=user.role.name, displayName=user.email
    )
    return UserLoginResponse(user=user_profile, token=access_token)
