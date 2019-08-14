FROM python:3.6-alpine
WORKDIR /app/api
COPY src/* Dockerfile requirements.txt /app/api/
COPY scripts/* /app/api/scripts/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD python scripts/wait-for-pg.py api-db && python app.py