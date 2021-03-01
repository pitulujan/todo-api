FROM python:3.6-alpine

RUN adduser -D martin

WORKDIR /home/martin

COPY enviroment enviroment
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip setuptools wheel
RUN venv/bin/pip install -r enviroment/req_deploy.txt
RUN venv/bin/pip install gunicorn 

COPY api api
COPY config config
COPY repos repos
COPY wsgi.py jwt-key jwt-key.pub .env ./

COPY boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP wsgi.py

RUN chown -R martin:martin ./
USER martin

RUN ls -la

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]