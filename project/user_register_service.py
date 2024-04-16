from typing import Optional

import prisma
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Response model for user registration. It confirms the user's registration status.
    """

    userId: str
    message: str
    status: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def user_register(
    email: str,
    password: str,
    fullName: Optional[str] = None,
    phoneNumber: Optional[str] = None,
) -> UserRegistrationResponse:
    """
    Handles new user registration by creating a new user record in the database with the provided details.
    The password is hashed for security before being stored. Optional fullName and phoneNumber can also be stored.

    Args:
        email (str): User's email address. It will be used as a unique identifier for the user.
        password (str): User's password in plaintext which will be hashed before being stored.
        fullName (Optional[str]): Full name of the user, optional field.
        phoneNumber (Optional[str]): User's phone number, optional for additional account security or recovery options.

    Returns:
        UserRegistrationResponse: Response model for user registration. It confirms the user's registration status.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return UserRegistrationResponse(
            userId="", message="Email already in use", status="Failed"
        )
    hashed_password = pwd_context.hash(password)
    try:
        user = await prisma.models.User.prisma().create(
            data={
                "email": email,
                "password": hashed_password,
                **({"full_name": fullName} if fullName is not None else {}),
                **({"phone_number": phoneNumber} if phoneNumber is not None else {}),
            }
        )
        return UserRegistrationResponse(
            userId=user.id, message="User successfully registered", status="Success"
        )
    except Exception as e:
        return UserRegistrationResponse(userId="", message=str(e), status="Failed")
