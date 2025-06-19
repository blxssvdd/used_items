from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str


class UserModelResponse(BaseModel):
    id: str
    username: str
    active: bool
    