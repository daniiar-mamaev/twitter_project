FROM python:3.11.3-alpine3.18

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc
RUN apk add python3-dev
RUN apk add postgresql-dev
RUN apk add musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/backend/entrypoint.sh"]