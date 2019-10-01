FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
ENV STATIC_URL app/static
ENV STATIC_PATH /app/static
COPY ./requirements.txt /requirements.txt
RUN pip install -r /var/www/requirements.txt
