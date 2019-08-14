FROM python:3.6-alpine
WORKDIR /app/auth
COPY src/* Dockerfile requirements.txt /app/auth/
COPY scripts/* /app/auth/scripts/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD python scripts/wait-for-pg.py -t 180 auth-db && python app.py