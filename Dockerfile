FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY ./Pipfile ./
COPY ./Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system --deploy

WORKDIR /src/app

COPY ./.env .

COPY ./ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]