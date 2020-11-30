# Base Image
FROM python:3.6

# # set default environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

# # create and set working directory
RUN mkdir /app
WORKDIR /app

# # Copy and Install system dependencies
ADD requirements.txt /app/
RUN pip install  --upgrade pip && pip install -r requirements.txt

ADD . /app/
EXPOSE 8000
EXPOSE 5000

