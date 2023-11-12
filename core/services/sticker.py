from rembg import remove
from PIL import Image
from io import BytesIO


async def create_sticker(input_path: str, name: str) -> None:
    """
    Removing background of the selected image and turn it into a png
    to make a sticker out of it.
    """
    with open(input_path, "rb") as input_file:
        input_data: bytes = input_file.read()

    output_data: bytes = remove(input_data)

    with Image.open(BytesIO(output_data)) as output_image:
        output_image.save(f"./static/stickers/{name}.png")
