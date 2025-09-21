from PIL import Image
import io, imagehash

def strip_exif(image_bytes: bytes) -> bytes:
    im = Image.open(io.BytesIO(image_bytes))
    data = list(im.getdata())
    im_no_exif = Image.new(im.mode, im.size)
    im_no_exif.putdata(data)
    buf = io.BytesIO()
    im_no_exif.save(buf, format=im.format or "JPEG", quality=85)
    return buf.getvalue()

def compute_phash(image_bytes: bytes) -> str:
    im = Image.open(io.BytesIO(image_bytes))
    return str(imagehash.phash(im))

def get_mime_from_bytes(image_bytes: bytes) -> str:
    im = Image.open(io.BytesIO(image_bytes))
    fmt = (im.format or "JPEG").lower()
    return f"image/{'jpeg' if fmt == 'jpg' else fmt}"
