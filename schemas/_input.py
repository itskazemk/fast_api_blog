from pydantic import BaseModel


class Register_DeleteInput(BaseModel):
    username: str
    password: str


class UpdateUserProfileInput(BaseModel):
    old_username: str
    new_username: str
