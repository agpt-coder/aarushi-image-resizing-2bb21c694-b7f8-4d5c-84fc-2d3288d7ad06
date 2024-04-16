from typing import Optional

import prisma
import prisma.models
from PIL import Image as PILImage
from pydantic import BaseModel


class ResizeImageResponse(BaseModel):
    """
    A model detailing the outcome of the image resize operation, including success status and details of the resized image.
    """

    success: bool
    message: str
    resized_image_path: Optional[str] = None
    resized_width: Optional[int] = None
    resized_height: Optional[int] = None


async def resize_image(
    image_id: str, desired_width: int, desired_height: int, maintain_aspect_ratio: bool
) -> ResizeImageResponse:
    """
    Endpoint for requesting image resizing with or without aspect ratio maintenance.

    Args:
        image_id (str): The unique identifier of the image to be resized.
        desired_width (int): The target width for the resized image.
        desired_height (int): The target height for the resized image.
        maintain_aspect_ratio (bool): A boolean option indicating whether the image's aspect ratio should be maintained during resizing.

    Returns:
        ResizeImageResponse: A model detailing the outcome of the image resize operation, including success status and details of the resized image.
    """
    image_record = await prisma.models.Image.prisma().find_unique(
        where={"id": image_id}
    )
    if not image_record:
        return ResizeImageResponse(
            success=False, message=f"Image with ID {image_id} not found."
        )
    original_image_path = (
        image_record.processedPath if image_record.processedPath else ""
    )
    try:
        with PILImage.open(original_image_path) as img:
            original_width, original_height = img.size
            if maintain_aspect_ratio:
                aspect_ratio = original_width / original_height
                if desired_width / desired_height > aspect_ratio:
                    new_height = desired_height
                    new_width = int(desired_height * aspect_ratio)
                else:
                    new_width = desired_width
                    new_height = int(desired_width / aspect_ratio)
            else:
                new_width, new_height = (desired_width, desired_height)
            img = img.resize((new_width, new_height), PILImage.LANCZOS)
            new_image_path = f"resized_images/{image_id}_resized.jpeg"
            img.save(new_image_path, "JPEG")
            return ResizeImageResponse(
                success=True,
                message="Image resized successfully.",
                resized_image_path=new_image_path,
                resized_width=new_width,
                resized_height=new_height,
            )
    except Exception as e:
        return ResizeImageResponse(success=False, message=str(e))
