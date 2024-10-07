FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY . .
RUN apk add build-base libpq-dev
RUN pip3 install -r req.txt
EXPOSE 3000