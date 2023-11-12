from typing import Any, Sequence, Tuple
from fastapi import HTTPException, UploadFile
from rembg import remove, new_session
from io import BytesIO
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.stickers import Stickers
from PIL import Image
import uuid


async def create_sticker(
    image: UploadFile, name: str, for_humans: bool = False
) -> None:
    """
    Removing background of the selected sticker and turn it into a png
    to make a sticker out of it.
    """

    # Read the content of the uploaded file
    if for_humans:
        model_name = "u2net_human_seg"
        session = new_session(model_name)
    sticker_content: bytes = await image.read()
    output_data: bytes = remove(
        sticker_content,
        alpha_matting=True,
        alpha_matting_erode_size=20 if for_humans else 10,
        session=session if for_humans else None,
    )
    with Image.open(BytesIO(output_data)) as output_sticker:
        output_sticker.save(f"./static/stickers/{name}.png")
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


async def get_all_stickers_from_db(db: AsyncSession) -> Sequence[Stickers]:
    """
    Get Stickers data from the database and return a list
    """
    # try:
    q: Result[Tuple[Stickers]] = await db.execute(select(Stickers))
    data: Sequence[Stickers] = q.scalars().all()
    return data
    # except Exception as error:
    #     raise HTTPException(status_code=404, detail="No Stickers Found") from error


async def get_single_sticker_from_db(id: int, db: AsyncSession) -> Stickers:
    """
    Get sticker data from the database and return
    """
    try:
        q: Result[Tuple[Stickers]] = await db.execute(select(Stickers).filter_by(id=id))
        data: Stickers | None = q.scalars().first()
        return data
    except Exception as error:
        raise HTTPException(status_code=404, detail="No sticker Found") from error
