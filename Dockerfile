FROM python:3.8-slim

WORKDIR /app

RUN pip install 'poetry>=1.0.0'
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY src/ ./src/

ENTRYPOINT [ "poetry", "run", "google-photos-archiver"]
CMD ["--help"]
