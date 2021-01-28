FROM python:3.8
WORKDIR /app

ADD requirements.txt /app
RUN python3 -m pip install -r requirements.txt

ADD . /app
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]