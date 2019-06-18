FROM python:3.7-alpine
LABEL Maintainer="imrim S.A." Author="Jacques Clément"

# Recommended that for Python, Docker should not buffer the output but rather put it out as it comes
ENV PYTHONUNBUFFERED 1

# Use the alpine package manager to install the PostgreSQL client (but do not cache to keep the image light)
RUN apk add --update --no-cache postgresql-client

# Add dependencies that are required to install the Python Postgresql module
# Option --virtual creates an alias that we can then use later to remove them and keep the 
# image light
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

# Now we can copy our Python requirements description file then run pip to install all the requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Python modules installed, we can remove the temp dependencies
RUN apk del .tmp-build-deps

# Create a directory for our app and move the workdir into it. Any application inside the container will run from this directory
RUN mkdir /app
WORKDIR /app

# Copy our app into it
COPY ./app /app

# Create a user that will run our application, and then switch to it (-D means create a user for running applications only)
# Not doing this would make the image running our app using root: not great
RUN adduser -D user
USER user





