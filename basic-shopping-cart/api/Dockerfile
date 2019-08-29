FROM python:3.6-alpine
WORKDIR /app/api
COPY api/src/* api/requirements.txt shared/src/*.py /app/api/
COPY shared/scripts/wait-for-pg.py /app/setup/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt && pip install gunicorn
EXPOSE 80
CMD python ../setup/wait-for-pg.py api-db && gunicorn -b 0.0.0.0:80 app:app