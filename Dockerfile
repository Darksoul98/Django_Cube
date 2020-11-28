# Base Image
FROM python:3.6

# create and set working directory
RUN mkdir /app

WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
# ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000

COPY requirements.txt ./
# Install system dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD exec gunicorn project.wsgi:application --bind 0.0.0.0:$PORT --workers 3