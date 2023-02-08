from httpx import AsyncClient


async def test_create_card(async_client: AsyncClient):
    """Test create card (auth user)"""
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


async def test_card_answer(async_client: AsyncClient):
    """Test update card after getting card answer (auth user)"""
    response = await async_client.post(
        url='/users/token/',
        data={"username": "new_test_user", "password": "1a2b3c"}
    )
    token = response.json()['access_token']

    card_previous_change = await async_client.get(
        url='/cards/',
        headers={'Authorization': f'Bearer {token}'}
    )
    card_previous_change = card_previous_change.json()[0]
    change_card = await async_client.put(
        url='/cards/answer/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'card_id': 1,
            'quality': 5,
        }
    )
    result = change_card.json()
    assert result['status'] == 'success'

    card_after_change = await async_client.get(
        url='/cards/',
        headers={'Authorization': f'Bearer {token}'}
    )
    card_after_change = card_after_change.json()[0]

    assert card_previous_change['easiness'] != card_after_change['easiness']
    assert card_previous_change['repetitions'] != card_after_change['repetitions']
    assert card_previous_change['interval'] != card_after_change['interval']
    assert card_previous_change['review_date'] != card_after_change['review_date']
