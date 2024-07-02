import logging
import os

from telegram.ext import Updater

from db_wrapper import DBWrapper
from handlers.user.help import HelpHandler
from handlers.user.admins import AdminsHandler
from handlers.user.all import AllHandler
from handlers.user.void import VoidHandler
from handlers.user.dice import DiceHandler
from handlers.admin.reset import ResetHandler
from handlers.admin.variable import VariableHandler
from handlers.admin.format import FormatHandler


TOKEN = os.environ.get("TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
DB_FILE = os.environ.get("DB_FILE")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=LOG_LEVEL if LOG_LEVEL else logging.INFO)


dbw = DBWrapper(DB_FILE)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
COMMANDS = [HelpHandler(dbw,updater),
            AdminsHandler(dbw, updater), AllHandler(dbw, updater), DiceHandler(dbw, updater),
            ResetHandler(dbw, updater), VariableHandler(dbw, updater), FormatHandler(dbw, updater),
            VoidHandler(dbw, updater)]

for command in COMMANDS:
    dispatcher.add_handler(command)

updater.start_polling()
