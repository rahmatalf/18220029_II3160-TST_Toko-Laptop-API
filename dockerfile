FROM python:3.8-slim

COPY ./src /app/src
COPY ./database /app/database
COPY ./requirements.txt /app
COPY ./.env /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
