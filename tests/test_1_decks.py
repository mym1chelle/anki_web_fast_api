from httpx import AsyncClient


async def test_create_deck(async_client: AsyncClient):
    """Test create deck (auth user)"""
    response = await async_client.post(
        url='/users/token/',
        data={"username": "new_test_user", "password": "1a2b3c"}
    )
    token = response.json()['access_token']
    await async_client.post(
        url='/decks/add/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'test_first_card'
        }
    )
    check_deck = await async_client.get(
        url='/decks/',
        headers={'Authorization': f'Bearer {token}'}
    )
    deck = check_deck.json()[0]
    assert deck['name'] == 'test_first_card'