FROM python:3.9.9-bullseye

COPY /appeals_writer /appeals_writer
COPY /common /common
COPY /models /models 

RUN apt update -y
RUN pip install --upgrade pip
RUN pip install -r /appeals_writer/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/../"

CMD [ "uvicorn", "appeals_writer.app:app"]