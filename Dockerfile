# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt entrypoint.sh src .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "./entrypoint.sh"]
