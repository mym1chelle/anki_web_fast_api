from conftest import client
from httpx import AsyncClient


def test_auth():
    response = client.post(
        url='/users/registration/',
        json={
            "username": "new_test_user",
            "password": "1a2b3c"
        }
    )
    new_user = response.json()
    assert response.status_code == 200
    assert new_user['id'] == 1
    assert new_user['username'] == 'new_test_user'
    assert new_user['decks'] == []


async def test_register(async_client: AsyncClient):
    response = await async_client.post(
        url='/users/token/',
        data={"username": "new_test_user", "password": "1a2b3c"}
    )
    token = response.json()['access_token']
    get_current_user = await async_client.get(
        url='/users/me/',
        headers={'Authorization': f'Bearer {token}'}
    )
    current_user = get_current_user.json()

    assert current_user['username'] == 'new_test_user'
    assert current_user['decks'] == []