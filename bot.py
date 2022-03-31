import logging
import os

from telegram.ext import Updater

from handlers.admins import AdminsHandler

TOKEN = os.environ.get("TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=LOG_LEVEL if LOG_LEVEL else logging.INFO)


updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
COMMANDS = [AdminsHandler(updater)]

for command in COMMANDS:
    dispatcher.add_handler(command)

updater.start_polling()
