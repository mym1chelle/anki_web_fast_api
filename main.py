from fastapi import FastAPI

from users.router import router as router_users
from cards.router import router as router_cards
from decks.router import router as router_decks
from card_styles.router import router as router_card_styles
from card_types.router import router as router_card_types

app = FastAPI(
    debug=True,
    title='Anki ASYNC v.1',
    description='API для приложения Anki'
)

app.include_router(
    router_users
)

app.include_router(
    router_cards
)

app.include_router(
    router_decks
)

app.include_router(
    router_card_styles
)

app.include_router(
    router_card_types
)
