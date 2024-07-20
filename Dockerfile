FROM alpine:latest

WORKDIR /app
COPY bot.py db_wrapper.py ./
COPY handlers/ handlers/

RUN apk add python3 py3-pip && pip install --break-system-packages python-telegram-bot --upgrade 

ENTRYPOINT [ "/usr/bin/python3", "/app/bot.py" ]