from pydantic import BaseModel

class FileRequest(BaseModel):
    filename: str
