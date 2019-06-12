FROM python:3.7-alpine
LABEL Maintainer="imrim S.A."

# Recommended that for Python, Docker should not buffer the output but rather put it out as it comes
ENV PYTHONUNBUFFERED 1

# Copy our Python requirements onto the image and then run pip to install them
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Create a directory for our app and move the workdir into it. Any application inside the container will run from this directory
RUN mkdir /app
WORKDIR /app

# Copy our app into it
COPY ./app /app

# Create a user that will run our application, and then switch to it (-D means create a user for running applications only)
# Not doing this would make the image running our app using root: not great
RUN adduser -D user
USER user





