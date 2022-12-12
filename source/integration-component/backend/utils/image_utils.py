import io
import os

import PIL.Image as Image


def save_byte_img(img: bytes, path: str):
    image = Image.open(io.BytesIO(img))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)
