FROM python:3.6
ENV PYTHONUNBUFFERED 1
ADD app/ /app
WORKDIR /app
RUN \
  touch mitaba/core/settings.py && \
  pip install -r requirements.txt -c constraints.txt
