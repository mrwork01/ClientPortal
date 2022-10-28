FROM python:3

RUN mkdir app
RUN cd app

ADD / /
ADD requirements.txt /

RUN pip3 install -r requirements.txt
RUN pip3 install -e /local_package/flask_security

CMD ["gunicorn", "run:server"]