import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers.user.custom_handler import CustomHandler


class GithubHandler(CustomHandler):

    COMMAND = 'github'
    TEXT = 'github.com/eryalito/fofonso'

    def __init__(self, dbw: DBWrapper, application: Application):
        super(GithubHandler, self).__init__(self.COMMAND, self.run, dbw)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + ' command has been called: ' + str(update.effective_chat.id))
        self.pre_command(update, context)
        await self.application.bot.sendMessage(update.effective_chat.id, self.TEXT)
