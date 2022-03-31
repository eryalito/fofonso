import json
import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater


class AdminsHandler(CommandHandler):

    COMMAND = 'admins'

    def __init__(self, updater: Updater):
        super(AdminsHandler, self).__init__(self.COMMAND, self.run)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if update.effective_message.chat.type == 'group':
            users_str = ""
            for admin in self.updater.bot.getChatAdministrators(update.effective_chat.id):
                if admin.user.username is not None:
                    users_str += '@' + admin.user.username + ' '
            if users_str:
                users_str = users_str[:-1]
                self.updater.bot.send_message(update.effective_chat.id, users_str)
