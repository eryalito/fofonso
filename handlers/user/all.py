import logging

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers.user.custom_handler import CustomHandler


class AllHandler(CustomHandler):

    COMMAND = 'all'

    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(AllHandler, self).__init__(self.COMMAND, self.run, dbw)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + ' command has been called: ' + str(update.effective_chat.id))
        self.pre_command(update, context)
        if update.effective_message.chat.type == 'group' or update.effective_message.chat.type == 'supergroup':
            users_str = ''
            for user in self.dbw.get_users_in_group(update.effective_chat.id):
                if 'username' in user:
                    users_str += '@' + user['username'] + ' '
            if users_str:
                users_str = users_str[:-1]
                self.updater.bot.send_message(update.effective_chat.id, users_str)
