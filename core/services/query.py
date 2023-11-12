from io import BytesIO
from typing import Sequence, Tuple
from fastapi import HTTPException, Response
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ReadTimeout
import uuid

from core.models.images import Images


class Query:
    """
    Hugging Face Model Query
    """

    def __init__(self, url: str, token: str, prompt: str) -> None:
        self.uuid: uuid.UUID = uuid.uuid4()
        self.url: str = url
        self.prompt: str = f"{prompt}, face, realistic, pixel art, profile, flat colors"
        self.headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
        self.path: str = f"./static/images/{str(self.uuid)}.jpeg"

    async def get_image(self) -> Response:
        """
        Get the image from the hugging face inference api using the hugging face
        token, the url of the specified model and the desired prompt.

        adding "face, realistic, pixel art, profile, flat colors" to the prompts
        for getting the best result to make a sticker.
        """
        try:
            async with AsyncClient() as client:
                response: Response = await client.post(
                    self.url,
                    headers=self.headers,
                    json=self.prompt,
                    timeout=10,
                )
                response.raise_for_status()
                return response
        except ReadTimeout as timeout_error:
            raise HTTPException(
                status_code=504, detail="Request to external server timed out"
            ) from timeout_error
        except Exception as error:
            raise HTTPException(
                status_code=500, detail="Internal server error"
            ) from error

    async def save_image(self, image: BytesIO) -> None:
        """
        Saving the image returned from the query to the server storage
        """
        try:
            # Read the data from BytesIO
            image_data: bytes = image.getvalue()
            # Save the image
            with open(self.path, "wb") as img_out:
                img_out.write(image_data)
            return
        except Exception as error:
            raise HTTPException(
                status_code=400, detail="Couldn't save the image"
            ) from error

    async def save_to_db(self, db: AsyncSession) -> None:
        """
        Saving the image returned from the query to the database.

        will include the image path and the prompt.
        """
        try:
            data: dict[str, str] = {
                "image": self.path.lstrip("."),
                "prompt": self.prompt,
            }
            add = Images(**data)
            db.add(add)
            await db.commit()
            await db.refresh(add)
        except Exception as error:
            raise HTTPException(
                status_code=400, detail="Couldn't save the image to database"
            ) from error


async def get_all_images_from_db(db: AsyncSession) -> Sequence[Images]:
    try:
        q: Result[Tuple[Images]] = await db.execute(select(Images))
        data: Sequence[Images] = q.scalars().all()
        return data
    except Exception as error:
        raise HTTPException(status_code=404, detail="No Images Found") from error
