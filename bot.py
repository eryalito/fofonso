import logging
import os

from telegram.ext import Updater

from db_wrapper import DBWrapper
from handlers.admins import AdminsHandler
from handlers.all import AllHandler
from handlers.void import VoidHandler

TOKEN = os.environ.get("TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
DB_FILE = os.environ.get("DB_FILE")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=LOG_LEVEL if LOG_LEVEL else logging.INFO)


dbw = DBWrapper(DB_FILE)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
COMMANDS = [AdminsHandler(dbw, updater), AllHandler(dbw, updater), VoidHandler(dbw, updater)]

for command in COMMANDS:
    dispatcher.add_handler(command)

updater.start_polling()
