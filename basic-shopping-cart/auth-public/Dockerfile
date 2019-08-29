FROM python:3.6-alpine
WORKDIR /app/auth
COPY auth-public/src/* auth-public/Dockerfile auth-public/requirements.txt /app/auth/
COPY shared/scripts/wait-for-api.py /app/setup/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt && pip install gunicorn
EXPOSE 80
CMD python ../setup/wait-for-api.py http://auth/ && gunicorn -b 0.0.0.0:80 app:app