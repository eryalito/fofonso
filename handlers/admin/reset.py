import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers.admin.admin_default_handler import AdminDefaultHandler


class ResetHandler(AdminDefaultHandler):

    COMMAND = 'reset'

    def __init__(self, dbw: DBWrapper, application: Application):
        super(ResetHandler, self).__init__(self.COMMAND, dbw, application)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if await self.is_valid(update, context):
            self.dbw.clean_users_from_group(update.effective_chat.id)
            await self.application.bot.sendMessage(update.effective_chat.id, "Chat reseted")
