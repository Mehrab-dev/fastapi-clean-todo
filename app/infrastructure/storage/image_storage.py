from fastapi import UploadFile
from pathlib import Path
from uuid import uuid4


UPLOAD_DIR = Path("uploads/profiles")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_profile_image(file: UploadFile) -> str:
    if file.filename is None:
        raise ValueError("file name is missing")
    extension = Path(file.filename).suffix
    filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / filename
    content = await file.read()

    with open(file_path, "wb") as image:
        image.write(content)

    return str(file_path)