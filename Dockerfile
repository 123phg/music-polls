FROM python:3.8.3-alpine
WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY ./entrypoint.sh .
RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev postgresql-libs \
    bash \
    && pip install --upgrade pip --no-cache-dir -r requirements.txt \
    && apk del gcc
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
