FROM python:latest

WORKDIR /app
COPY . .
RUN pip install -r req.txt
EXPOSE 3000