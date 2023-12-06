from uuid import UUID

from pydantic import BaseModel


class Register_DeleteOutput(BaseModel):
    id: UUID
    username: str
