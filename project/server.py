import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.resize_image_service
import project.session_renewal_service
import project.upload_image_service
import project.user_login_service
import project.user_register_service
from fastapi import FastAPI, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-image-resizing-2",
    lifespan=lifespan,
    description="The task involves developing a feature that processes an uploaded image according to user-defined dimensions, incorporating both resizing and optional aspect ratio maintenance through cropping. To achieve this, we'll leverage Python as the chosen programming language due to its robust support for image manipulation, alongside libraries and techniques previously identified.\n\n**Key Requirements & Implementation Steps:**\n1. Accept JPEG images from users, supporting a common use case of web-oriented image handling.\n2. Utilize Python's Pillow library, which provides comprehensive tools for image resizing and cropping while maintaining excellent performance and quality outcomes.\n3. Implement functionality to resize images to a target dimension of 1080x720 pixels, a size that optimally balances quality and file size for both web and print media.\n4. Incorporate a cropping feature that maintains the original image's aspect ratio, should the user opt for this. This entails calculating the target aspect ratio based on user input, cropping the image accordingly, and ensuring the final image matches the desired dimensions closely without distorting the original content's proportions.\n5. Apply best practices for image resizing and cropping, such as selecting the appropriate algorithm for resizing (e.g., bicubic, bilinear) to maintain quality, applying sharpening post-resize to enhance clarity, and considering the final format and compression to optimize for both quality and file size efficiency.\n\nThe development stack includes FastAPI to handle HTTP requests for image uploads and processing responses efficiently, PostgreSQL for any needed image metadata storage, and Prisma as the ORM for robust database interactions. This tech stack is selected for its ease of use, performance, and scalability, which aligns well with the project's needs for handling image manipulation tasks.",
)


@app.post(
    "/image/resize", response_model=project.resize_image_service.ResizeImageResponse
)
async def api_post_resize_image(
    desired_width: int, desired_height: int, maintain_aspect_ratio: bool, image_id: str
) -> project.resize_image_service.ResizeImageResponse | Response:
    """
    Endpoint for requesting image resizing with or without aspect ratio maintenance
    """
    try:
        res = await project.resize_image_service.resize_image(
            desired_width, desired_height, maintain_aspect_ratio, image_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/session/renew",
    response_model=project.session_renewal_service.SessionRenewalResponse,
)
async def api_post_session_renewal(
    session_id: str, auth_token: str
) -> project.session_renewal_service.SessionRenewalResponse | Response:
    """
    Renews user session for active users
    """
    try:
        res = await project.session_renewal_service.session_renewal(
            session_id, auth_token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/register",
    response_model=project.user_register_service.UserRegistrationResponse,
)
async def api_post_user_register(
    email: str, password: str, fullName: Optional[str], phoneNumber: Optional[str]
) -> project.user_register_service.UserRegistrationResponse | Response:
    """
    Handles new user registration
    """
    try:
        res = await project.user_register_service.user_register(
            email, password, fullName, phoneNumber
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Handles user login requests
    """
    try:
        res = await project.user_login_service.user_login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/image/upload", response_model=project.upload_image_service.ImageUploadResponse
)
async def api_post_upload_image(
    image: UploadFile, format: Optional[str]
) -> project.upload_image_service.ImageUploadResponse | Response:
    """
    Endpoint for image upload and preliminary validation
    """
    try:
        res = await project.upload_image_service.upload_image(image, format)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
