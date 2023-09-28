import pytest
import requests

from app.api.routes.clients import create_client, one_client
from app.models.client import ClientIn, ClientOut


@pytest.fixture()
def client() -> ClientIn:
    return ClientIn(id='1', name='name', surname='surname',)


@pytest.mark.asyncio
async def test_create(client_in: ClientIn):
    response: ClientOut = await create_client(client_in)
    assert response == client_in


@pytest.mark.asyncio
async def test_read(client: ClientIn):
    response = one_client(client.client_id)
    assert response == client


@pytest.mark.asyncio
async def test_read_wrong_id():
    response = one_client(rand_int())
    assert response == client


@pytest.mark.asyncio
async def test_update(client: ClientIn):
    client = {
        'id': str(client.id),
        'name': client.name,
        'surname': 'new surname',
        'department': client.department,
        'position': client.position
    }
    response = requests.put(base_url + '/', json=client)
    assert response.status_code == 200
    assert response.json() == client

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
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'client_id': str(client.id)})
    response = requests.delete(base_url + '/%7Bid%7D?', params={'client_id': str(client.id)})
    assert response.status_code == 200
    assert response.json() == get_response.json()
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'client_id': str(client.id)})
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_wrong_id(client: ClientIn):
    response = requests.delete(base_url + '/%7Bid%7D?', params={'client_id': str(client.id)})
    assert response.status_code == 404
