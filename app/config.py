import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

allowed_content_types = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
}
