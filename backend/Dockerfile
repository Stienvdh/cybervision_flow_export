FROM python:3.9.16-slim

COPY . .

RUN apt-get update && apt-get install -y cron

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN chmod 0644 crontab 

RUN crontab crontab

CMD ["cron","-f", "-l", "2"] 
