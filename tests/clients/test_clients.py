import pytest
import pytest_asyncio
import requests
from app.api.routes.clients import create_client, one_client, delete_client, update_client
from app.models.client import ClientIn, ClientOut
from app.db.base import database



@pytest.fixture
def client() -> ClientIn:
    return ClientIn(id='1',
                    name='name',
                    password="password",
                    surname='surname',
                    patronomic="patronomic",
                    photo="path",
                    phone="8-800-000-00-00",
                    email="email",
                    )


@pytest_asyncio.fixture
async def db_connection():
    await database.connect()
    yield
    await database.disconnect()


@pytest_asyncio.fixture
async def db_client(db_connection, client: ClientIn):
    client: ClientOut = await create_client(client)
    yield client
    await delete_client(client.id)


@pytest.mark.asyncio
async def test_create(db_connection, client: ClientIn):
    response: ClientOut = await create_client(client)
    assert response == ClientOut(**client.dict())


@pytest.mark.asyncio
async def test_read(db_connection, db_client: ClientIn):
    response = await one_client(db_client.id)
    assert response == ClientOut(**db_client .dict())


@pytest.mark.asyncio
async def test_update(db_connection, db_client: ClientIn):
    updated_client = ClientIn(
                              id='1',
                              name='update_name',
                              password="update_password",
                              surname='update_surname',
                              patronomic="update_patronomic",
                              photo="update_path",
                              phone="8-800-000-00-11",
                              email="update_email",
                              )
    client_after_update = await update_client(updated_client)
    assert client_after_update == updated_client

@pytest.mark.asyncio
async def test_update_wrong_id(client: ClientIn):
    client = {
        'id': '21111111-1111-1111-1111-111111111111',
        'name': client.name,
        'surname': 'new surname',
        'department': client.department,
        'position': client.position
    }
    response = requests.put(base_url + '/', json=client)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete(client: ClientIn):
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'id': str(client.id)})
    response = requests.delete(base_url + '/%7Bid%7D?', params={'id': str(client.id)})
    assert response.status_code == 200
    assert response.json() == get_response.json()
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'id': str(client.id)})
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_wrong_id(client: ClientIn):
    response = requests.delete(base_url + '/%7Bid%7D?', params={'id': str(client.id)})
    assert response.status_code == 404
