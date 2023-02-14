# pull the official base image
FROM python:3.10-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*


# copy project into images
RUN mkdir -p /project
COPY . /project/.

# set working directory
WORKDIR /project

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker build --tag django_todo:latest .
# docker run --name django_todo -d -p 8000:8000 django_todo:latest
