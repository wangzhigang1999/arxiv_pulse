FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY arxiv_pulse/ arxiv_pulse/

CMD ["arxiv-pulse"]

