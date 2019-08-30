FROM python:3.6-alpine
WORKDIR /app/auth
COPY auth/src/ auth/requirements.txt ./
COPY shared/src/ shared/
COPY shared/scripts/wait-for-pg.py setup/
RUN find . -type f -print0 | xargs -0 dos2unix
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt && pip install gunicorn
EXPOSE 80
CMD python setup/wait-for-pg.py -t 180 auth-db && gunicorn -b 0.0.0.0:80 app:app