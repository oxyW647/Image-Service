from PIL import Image
from io import BytesIO


def convert_image(image: bytes, mode: str = "FLOYDSTEINBERG") -> dict:
    if mode == "FLOYDSTEINBERG":
        img = Image.open(BytesIO(image)).convert("1", dither=Image.FLOYDSTEINBERG)
    elif mode == "NONE":
        img = Image.open(BytesIO(image)).convert("1", dither=Image.NONE)
    else:
        raise ValueError("Unsupported dithering mode. Use 'FLOYDSTEINBERG' or 'NONE'.")
    img_width, img_height = img.size
    img_aspect_ratio = img_height / img_width
    img = img.resize((144, int(144 * img_aspect_ratio)))

    width, height = img.size
    width_bytes = (width + 7) // 8
    pixels = img.load()
    data = []

    for y in range(height):
        for byte in range(width_bytes):
            byte_value = 0
            for bit in range(8):
                x = byte * 8 + bit
                if x < width and pixels[x, y] == 0:
                    byte_value |= 1 << (7 - bit)
            data.append(byte_value)

    return {"data": data, "width": width, "height": height, "size": (len(data) * 8)}
