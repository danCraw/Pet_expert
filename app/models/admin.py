from app.models.base import BaseSchema


class AdminBase(BaseSchema):
    admin_id: int


class AdminIn(AdminBase):
    pass


class AdminOut(AdminBase):
    pass
