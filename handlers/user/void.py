import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater, Filters
from handlers.user.custom_handler import CustomMessageHandler

class VoidHandler(CustomMessageHandler):

    COMMAND = "void"

    
    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(VoidHandler, self).__init__(Filters.all, self.run, dbw)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        self.pre_command(update, context)
