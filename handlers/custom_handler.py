from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


class CustomHandler(CommandHandler):

    def __init__(self, command: str, callback: any, dbw: DBWrapper):
        super(CustomHandler, self).__init__(command, callback)
        self.dbw = dbw

    def pre_command(self, update: Update, context: CallbackContext):
        self.dbw.add_user(update.effective_message.from_user.id, update.effective_message.from_user.username)
        print(update.effective_chat.type)
        if update.effective_chat.type == 'group' or update.effective_chat.type == 'supergroup':
            self.dbw.add_user_to_group(update.effective_message.from_user.id, update.effective_chat.id)
