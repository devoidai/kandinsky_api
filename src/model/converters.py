import io
import os
import base64

from PIL import Image

def load_image(file_name) -> Image:
    path = os.getenv('IMAGES_PATH') + file_name
    if not os.path.isdir(path):
        raise FileNotFoundError(f'Image with path "{path}" not exists')
    with open(path, 'rb') as file:
        image = Image.open(io.BytesIO(file))
    return image

def image_to_bytes(image: Image) -> bytes:
    bytes_arr = io.BytesIO()
    image.save(bytes_arr, 'JPEG')
    img_bytes = bytes_arr.getvalue()
    return img_bytes

def image_to_base64_str(image: Image) -> str:
    image = image_to_bytes(image)
    base64_bytes = base64.b64encode(image)
    return base64_bytes.decode('UTF-8')

def base64_str_to_image(base64_image: str) -> Image:
    bytesIO = io.BytesIO(base64.b64decode(base64_image))
    return Image.open(bytesIO)