import io
import uuid
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from fastapi import UploadFile
from PIL import Image as PILImage
from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    """
    Response model confirming the image upload with preliminary validation results.
    """

    upload_id: str
    validation_status: str
    message: Optional[str] = None


async def upload_image(
    image: UploadFile, format: Optional[str] = None
) -> ImageUploadResponse:
    """
    Endpoint for image upload and preliminary validation. It handles image resizing and optional reformatting.

    This function initiates by validating the uploaded image's format. It supports JPEG and PNG formats
    for the input image. The image is then resized to a standard dimension of 1080x720 pixels,
    maintaining the aspect ratio. Optionally, the image can be converted to a different format
    specified by the user.

    Args:
        image (UploadFile): The image file being uploaded.
        format (Optional[str]): Optional. The desired format of the output image, e.g., JPEG, PNG, WEBP.

    Returns:
        ImageUploadResponse: Response model confirming the image upload with preliminary validation results.

    Raises:
        ValueError: If the uploaded file format is not supported or if the requested format conversion is not supported.
    """
    if image.content_type not in ["image/jpeg", "image/png"]:
        return ImageUploadResponse(
            upload_id=str(uuid.uuid4()),
            validation_status="Failed",
            message="Unsupported image format.",
        )
    image_data = await image.read()
    pil_image = PILImage.open(io.BytesIO(image_data))
    target_dimensions = (1080, 720)
    pil_image.thumbnail(
        target_dimensions, PILImage.ANTIALIAS
    )  # TODO(autogpt): "ANTIALIAS" is not a known member of module "PIL.Image". reportAttributeAccessIssue
    output_format = (
        format.upper()
        if format is not None
        else image.content_type.split("/")[-1].upper()
    )
    if output_format not in ["JPEG", "PNG", "WEBP"]:
        return ImageUploadResponse(
            upload_id=str(uuid.uuid4()),
            validation_status="Failed",
            message=f"Requested format {output_format} is not supported for conversion.",
        )
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format=output_format)
    img_bytes.seek(0)
    upload_id = str(uuid.uuid4())
    processed_image = await prisma.models.Image.prisma().create(
        data={
            "id": upload_id,
            "originalName": image.filename,
            "format": prisma.enums.ImageFormat(output_format),
            "status": prisma.enums.ImageStatus.PENDING,
            "width": pil_image.width,
            "height": pil_image.height,
            "maintainRatio": True,
            "processedPath": f"processed_images/{upload_id}.{output_format.lower()}",
        }
    )
    return ImageUploadResponse(
        upload_id=upload_id,
        validation_status="Success",
        message="Image uploaded and resized.",
    )
