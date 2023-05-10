
FROM python:3

RUN mkdir  /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#ENTRYPOINT ["chmod", "+x", "/app/entrypoint.sh"]