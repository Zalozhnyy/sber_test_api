FROM python:3.10

WORKDIR /src
ADD ./requirements.txt /src/requirements.txt

RUN pip install -r requirements.txt
ADD . /src

CMD [ "python", "-u", "start_app.py" ]