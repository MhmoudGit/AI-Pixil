from typing import Any
from fastapi import HTTPException, UploadFile
from rembg import remove
from PIL import Image
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.stickers import Stickers
import uuid


async def create_sticker(image: UploadFile, name: str) -> None:
    """
    Removing background of the selected image and turn it into a png
    to make a sticker out of it.
    """

    # Read the content of the uploaded file
    image_content: bytes = await image.read()
    output_data: bytes = remove(image_content)
    with Image.open(BytesIO(output_data)) as output_image:
        output_image.save(f"./static/stickers/{name}.png")
    return f"./static/stickers/{name}.png"


async def save_sticker_to_db(path: str, name: str, db: AsyncSession) -> None:
    """
    Saving the sticker to the database.

    will include the sticker path and the prompt.
    """
    random_uuid: Any = uuid.uuid4()
    try:
        data: dict[str, str] = {
            "sticker": path.lstrip("."),
            "name": f"{name}-{random_uuid}",
        }
        add = Stickers(**data)
        db.add(add)
        await db.commit()
        await db.refresh(add)
    except Exception as error:
        raise HTTPException(
            status_code=400, detail="Couldn't save sticker to database"
        ) from error
