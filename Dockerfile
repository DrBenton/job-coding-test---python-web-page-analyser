FROM alpine:3.6

# Python 3 install
RUN apk update \
  && apk add --no-cache \
    curl \
    python3

# Install pip and pipenv
RUN curl -o /get-pip.py https://bootstrap.pypa.io/get-pip.py && python3 /get-pip.py && rm /get-pip.py
RUN python3 -m pip install pipenv
