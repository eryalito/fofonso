import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers.user.custom_handler import CustomHandler


class AdminDefaultHandler(CustomHandler):

    def __init__(self, command: str, dbw: DBWrapper, application: Application):
        super(AdminDefaultHandler, self).__init__(command, self.run, dbw)
        self.application = application

    async def is_valid(self, update: Update, context: CallbackContext) -> bool:
        is_admin = False
        self.pre_command(update, context)
        if update.effective_message.chat.type == 'group' or update.effective_message.chat.type == 'supergroup':
            for admin in await self.application.bot.getChatAdministrators(update.effective_chat.id):
                if admin.user.id == update.effective_user.id:
                    is_admin = True
            # if not is_admin:
            #     await self.application.bot.sendMessage(update.effective_chat.id, "You need to be an administrator to run this command")
        return is_admin
