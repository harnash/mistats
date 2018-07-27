FROM python:3.6

ADD Pipfile* /service/
ADD server /service/server

RUN pip3 install pipenv

WORKDIR /service 
RUN pipenv install --system

EXPOSE 8080

VOLUME ["/data"]
ENV SERVER_PORT=8080
ENV LOG_MODE=json
ENV DEBUG_MODE=0
ENV SQLALCHEMY_DATABASE_URI=sqlite:////data/db.sqlite
ENV SECRET_KEY=change_me!

ENTRYPOINT ["hug", "-f", "/service/server/main.py"]