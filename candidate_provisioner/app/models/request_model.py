from pydantic import BaseModel


class FileRequest(BaseModel):
    filename: str
    email: str
    name: str
    phone: str
