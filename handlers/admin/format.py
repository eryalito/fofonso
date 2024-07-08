import logging
import traceback

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers import utils
from handlers.admin.admin_default_handler import AdminDefaultHandler


class FormatHandler(AdminDefaultHandler):

    COMMAND = 'format'
    COMMAND_LENGTH = len(COMMAND) + 1 # /COMMAND

    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(FormatHandler, self).__init__(self.COMMAND, dbw, updater)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if self.is_valid(update, context):
            command = update.message.text
            text_to_format = command[self.COMMAND_LENGTH:].strip()
            
            try:
                formatted_text = utils.format_text_for_group(update.effective_chat.id, text_to_format, self.dbw)
                self.updater.bot.send_message(update.effective_chat.id, formatted_text)
                try:
                    self.updater.bot.delete_message(update.effective_chat.id,update.effective_message.message_id)
                except:
                    logging.debug("Errror deleting message")
                    
            except:
                traceback.print_exc()
                self.updater.bot.send_message(update.effective_chat.id,"Error parsing the format text")
