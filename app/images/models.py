from beanie import Document
from pydantic import Field
from datetime import datetime


class Image(Document):
    image: bytes
    user: str
    width: int
    height: int
    size: int
    mode: str = Field(default="FLOYDSTEINBERG")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "images"
        indexes = ["user", "created_at"]
