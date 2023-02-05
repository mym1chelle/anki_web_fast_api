run:
	poetry run uvicorn main:app --reload

migrations:
	poetry run alembic init -t async migrations

revision:
	poetry run alembic revision --autogenerate

test:
	poetry run pytest -v -s
