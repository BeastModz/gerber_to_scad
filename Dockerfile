# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

ENV SCAD_BINARY=openscad DEBUG=False

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git gcc openscad curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN poetry config virtualenvs.create false && \
    poetry install -v --no-interaction --no-ansi

# Collect static files for Django
RUN python manage.py collectstatic --noinput --settings=gts_service.railway_settings || echo "Static files collection skipped"

# Expose port 8000
EXPOSE 8000

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD gunicorn --workers 1 --threads 8 --bind :${PORT:-8000} gts_service.wsgi
