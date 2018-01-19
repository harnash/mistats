FROM python:3-slim

ADD requirements.txt tmp/requirements.txt
ADD server service

RUN pip3 install -r /tmp/requirements.txt

EXPOSE 80

ENTRYPOINT ["python3", "/service/main.py"]