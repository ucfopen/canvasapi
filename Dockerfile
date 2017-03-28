FROM python:2.7.12-alpine

RUN apk update && apk add \
  gcc

# Add requirements files from app.
COPY requirements.txt /tmp/requirements.txt
COPY tests_requirements.txt /tmp/tests_requirements.txt

# Install all the requirements.
RUN pip install -r /tmp/tests_requirements.txt

WORKDIR /app
