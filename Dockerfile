FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.0 /uv /uvx /bin/
WORKDIR /app
ADD . /app
RUN uv sync --locked

CMD ["uv", "run", "-m", "src.main"]