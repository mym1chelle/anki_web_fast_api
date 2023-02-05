from httpx import AsyncClient


async def test_create_card(async_client: AsyncClient):
    response = await async_client.post(
        url='/users/token/',
        data={"username": "new_test_user", "password": "1a2b3c"}
    )
    token = response.json()['access_token']
    await async_client.post(
        url='/cards/add/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "question": "test_question",
            "question_type": 1,
            "answer": "test_answer",
            "answer_type": 1,
            "style": 1,
            "deck_id": 1
        }
    )
    check_card = await async_client.get(
        url='/cards/',
        headers={'Authorization': f'Bearer {token}'}
    )
    card = check_card.json()[0]
    assert card['question'] == 'test_question'
    assert card['answer'] == 'test_answer'
