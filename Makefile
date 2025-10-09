coverage:
	pytest --asyncio-mode=auto --cov=src --cov-report=xml

test:
	pytest --asyncio-mode=auto tests

run:
	python -m src.main
