import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application, filters
from handlers.user.custom_handler import CustomMessageHandler


class VoidHandler(CustomMessageHandler):

    COMMAND = "void"

    def __init__(self, dbw: DBWrapper, application: Application):
        super(VoidHandler, self).__init__(filters.ALL, self.run, dbw)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        self.pre_command(update, context)
