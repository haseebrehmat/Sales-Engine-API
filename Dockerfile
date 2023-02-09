# pull official base image
FROM python:3.10

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

#EXPOSE 8000
#CMD ["python", "manage.py", "runserver","--settings=settings.production" ,"0.0.0.0:8000"]
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mysite.wsgi:application"]
