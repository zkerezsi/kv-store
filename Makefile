coverage:
	pytest --asyncio-mode=auto --cov=src --cov-report=xml

test:
	pytest --asyncio-mode=auto tests

run:
	CLI_ENABLED=true uv run -m src.main
