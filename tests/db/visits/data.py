import pytest_asyncio

from app.api.routes.visits import delete_visit, create_visit
from app.models.visit import VisitIn, VisitOut
from tests.db.connection import db_connection
from tests.db.hospitals.data import db_hospital
from tests.db.doctors.data import db_doctor
from tests.db.clients.data import db_client


@pytest_asyncio.fixture
async def db_visit(db_connection, db_hospital, db_doctor, db_client, visit: VisitIn):
    visit: VisitOut = await create_visit(visit)
    yield visit
    await delete_visit(visit.id)
