FROM python:3.10

ARG SETTINGS
ENV MICROSERVICE=/home/app/microservice/
ENV SETTINGS=${SETTINGS}

RUN mkdir -p $MICROSERVICE
RUN mkdir -p $MICROSERVICE/static

WORKDIR $MICROSERVICE

RUN apt-get update \
    && apt-get -y install libpq-dev gcc gdal-bin logrotate \
    && pip install psycopg2

COPY ./requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8002

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Copy the start script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Use the start script to launch the application
CMD ["/start.sh"]
