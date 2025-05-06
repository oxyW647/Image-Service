from pydantic import BaseModel


class CreateImage(BaseModel):
    image: bytes
    user: str
    width: int
    height: int
    size: int
    mode: str = "FLOYDSTEINBERG"

    class Config:
        json_schema_extra = {
            "example": {
                "image": [],
                "whith": 384,
                "height": 384,
                "size": 147456,
            }
        }
