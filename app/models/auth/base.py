from pydantic import BaseModel


class Token(BaseModel):
    token: str


class IdModel(Token):
    id: int
