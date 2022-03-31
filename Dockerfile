FROM alpine:latest

WORKDIR /app
COPY bot.py .
COPY handlers/ handlers/

RUN apk add python3 py3-pip && pip install python-telegram-bot --upgrade 

ENTRYPOINT [ "/usr/bin/python3", "/app/bot.py" ]