import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers.admin.admin_default_handler import AdminDefaultHandler


class ResetHandler(AdminDefaultHandler):

    COMMAND = 'reset'

    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(ResetHandler, self).__init__(self.COMMAND, dbw, updater)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if self.is_valid(update, context):
            self.dbw.clean_users_from_group(update.effective_chat.id)
            self.updater.bot.send_message(update.effective_chat.id, "Chat reseted")
