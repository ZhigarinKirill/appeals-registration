FROM python:3.9.9-bullseye

COPY /api /api
COPY /common /common 

RUN apt update -y
RUN pip install --upgrade pip
RUN pip install -r /api/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/../"

CMD [ "python", "api"]