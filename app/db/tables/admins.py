from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.clients import clients

admins = Table(
    'admins',
    metadata,
    Column("admin_id", Integer, ForeignKey(clients.columns.id), nullable=False)
)
