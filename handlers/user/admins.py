import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers.user.custom_handler import CustomHandler


class AdminsHandler(CustomHandler):

    COMMAND = 'admins'

    def __init__(self, dbw: DBWrapper, application: Application):
        super(AdminsHandler, self).__init__(self.COMMAND, self.run, dbw)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        self.pre_command(update, context)
        if update.effective_message.chat.type == 'group' or update.effective_message.chat.type == 'supergroup':
            users_str = ""
            for admin in await self.application.bot.getChatAdministrators(update.effective_chat.id):
                if admin.user.username is not None:
                    users_str += '@' + admin.user.username + ' '
            if users_str:
                users_str = users_str[:-1]
                await self.application.bot.sendMessage(update.effective_chat.id, users_str)
