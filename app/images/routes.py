from fastapi import APIRouter, UploadFile, HTTPException, Form
from app.images.models import Image
from app.images.schemas import CreateImage
from app.images.utils import convert_image
from app.images.executor import AsyncExecutor
from app.config import allowed_content_types

router = APIRouter()

image_executor = AsyncExecutor()


@router.post("/upload")
async def upload_image(
    image: UploadFile,
    user: str = Form(...),
    mode: str = Form("FLOYDSTEINBERG"),
) -> dict:
    if image.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed types: JPEG, PNG, WEBP, BMP.",
        )
    try:
        bitmap = await image_executor.run(convert_image, image.file.read(), mode=mode)
        doc_template = CreateImage(
            user=user,
            image=bytes(bitmap["data"]),
            width=bitmap["width"],
            height=bitmap["height"],
            size=bitmap["size"],
            mode=mode,
        )
        doc = Image(**doc_template.dict())
        await doc.insert()
        return {"message": "Image uploaded successfully", "image_id": str(doc.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{image_id}")
async def get_image(image_id: str):
    try:
        doc = await Image.get(image_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Image not found")
        return {"image": list(doc.image), "width": doc.width, "height": doc.height}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
