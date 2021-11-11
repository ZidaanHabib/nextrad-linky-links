FROM balenalib/raspberrypi4-64-debian-python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app/
WORKDIR /app

CMD ["python3", "-u", "app.py"]