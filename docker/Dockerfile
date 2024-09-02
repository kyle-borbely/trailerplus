FROM python:3.8

RUN mkdir /app
WORKDIR app

# Copy project directory, Pipfile and Pipfile.lock to app
ADD trailersplus /app/
ADD Pipfile Pipfile.lock /app/

# SetUp environment veriables
# Disable creating .pyc files
ENV PYTHONDONTWRITBYTECODE 1
# Force the stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
# Use default answers for all questions
ENV DEBIAN_FRONTEND=noninteractive

# Install all dependencies
RUN pip3 install --upgrade pip &&\
    pip3 install pipenv &&\
    pipenv sync

EXPOSE 8888
