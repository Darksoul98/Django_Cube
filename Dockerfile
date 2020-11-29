# # Base Image
# FROM python:3.6

# # create and set working directory
# RUN mkdir /app

# WORKDIR /app

# # Add current directory code to working directory
# ADD . /app/

# # set default environment variables
# ENV PYTHONUNBUFFERED 1
# ENV 
# ENV LANG C.UTF-8
# # ENV DEBIAN_FRONTEND=noninteractive 

# # set project environment variables
# # grab these via Python's os.environ
# # these are 100% optional here
# ENV PORT=8000

# COPY requirements.txt ./
# # Install system dependencies
# RUN pip3 install -r requirements.txt

# EXPOSE 8000
# CMD exec python manage.py process_tasks
# CMD exec gunicorn project.wsgi:application --bind 0.0.0.0:$PORT --workers 3
FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

RUN mkdir /app
# RUN mkdir /code
WORKDIR /app
ADD requirements.txt /app/
RUN pip install  --upgrade pip && pip install -r requirements.txt
ADD . /app/

# WORKDIR /code
# ADD requirements.txt /code/
# RUN pip install  --upgrade pip && pip install -r requirements.txt
# ADD . /code/

EXPOSE 8000
EXPOSE 5000

