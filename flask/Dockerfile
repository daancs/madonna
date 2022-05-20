# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt usr/src/app/requirements.txt

ENV FLASK_APP "flaskr"
ENV FLASK_ENV "development"
ENV DB_PASSWORD "postgres"
ENV DB_HOST "madonna-db"

# switch working directory
WORKDIR /usr/src/app

# install the dependencies and packages in the requirements file
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


# copy every content from the local file to the image
COPY . /usr/src/app

EXPOSE 5000

# RUN flask init-db

# RUN flask register dadi 123
