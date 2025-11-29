FROM ghcr.io/astral-sh/uv:python3.12-alpine

LABEL maintainer="artem"

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY ./scripts /scripts

RUN apk add --update --no-cache \
        postgresql-client font-dejavu \
        build-base postgresql-dev musl-dev linux-headers && \
    adduser --disabled-password --home /app/home app && \
    mkdir -p /vol/web/static /vol/web/media /app/logs /app/home/.cache/uv && \
    chmod -R +x /scripts

COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev && \
    chown -R app:app /app /vol /app/logs /app/home/.cache && \
    chmod -R 755 /app/logs /vol

USER app

# Make sure the venv binaries are in PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_CACHE_DIR=/app/home/.cache/uv

EXPOSE 8000

CMD ["scripts/run.sh"]
