from pydantic import BaseModel

from app.models.client import ClientUpdate


class UpdateClient(BaseModel):
    token: str
    client: ClientUpdate
