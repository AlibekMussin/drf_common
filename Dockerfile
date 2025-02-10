FROM python:3.11.3-slim

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install nano -y && apt-get install curl -y

COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .
# create logs directory
RUN mkdir -p logs

#COPY ./static /var/static
RUN python manage.py collectstatic --no-input

#RUN #apt install -y ca-certificates &&  \
#    cp USIAG.crt /usr/local/share/ca-certificates/ && ls /usr/local/share/ca-certificates/ &&  \
#    update-ca-certificates

CMD gunicorn -b 0.0.0.0:8012 project.wsgi --timeout 600