FROM python:3.9.16-bullseye

EXPOSE 8888/tcp

COPY . .

RUN pip3 install -r requirements.txt

CMD python3 app.py