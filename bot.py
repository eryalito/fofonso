import logging
import os

from telegram.ext import Application
from db_wrapper import DBWrapper
from handlers.user.help import HelpHandler
from handlers.user.admins import AdminsHandler
from handlers.user.all import AllHandler
from handlers.user.void import VoidHandler
from handlers.user.dice import DiceHandler
from handlers.user.exclamation import ExclamationHandler
from handlers.user.github import GithubHandler
from handlers.admin.reset import ResetHandler
from handlers.admin.variable import VariableHandler
from handlers.admin.format import FormatHandler
from handlers.admin.alias import AliasHandler


TOKEN = os.environ.get("TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
DB_FILE = os.environ.get("DB_FILE")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=LOG_LEVEL if LOG_LEVEL else logging.INFO)


dbw = DBWrapper(DB_FILE)
application = Application.builder().token(TOKEN).build()
COMMANDS = [HelpHandler(dbw, application),
            # Admins
            AdminsHandler(dbw, application), AllHandler(dbw, application), DiceHandler(dbw, application), AliasHandler(dbw, application),
            # User
            ResetHandler(dbw, application), VariableHandler(dbw, application), FormatHandler(dbw, application), GithubHandler(dbw, application),
            # Exclamation command
            ExclamationHandler(dbw, application),
            # Default
            VoidHandler(dbw, application)]

for command in COMMANDS:
    application.add_handler(command)

application.run_polling()
