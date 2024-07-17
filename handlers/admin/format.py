import logging
import traceback

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers import utils
from handlers.admin.admin_default_handler import AdminDefaultHandler


class FormatHandler(AdminDefaultHandler):

    COMMAND = 'format'
    COMMAND_LENGTH = len(COMMAND) + 1  # /COMMAND

    def __init__(self, dbw: DBWrapper, application: Application):
        super(FormatHandler, self).__init__(self.COMMAND, dbw, application)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if await self.is_valid(update, context):
            command = update.message.text
            text_to_format = command[self.COMMAND_LENGTH:].strip()

            try:
                formatted_text = utils.format_text_for_group(update.effective_chat.id, text_to_format, self.dbw)
                await self.application.bot.sendMessage(update.effective_chat.id, formatted_text)
                try:
                    self.application.bot.delete_message(update.effective_chat.id, update.effective_message.message_id)
                except Exception:
                    logging.debug("Errror deleting message")

            except Exception:
                traceback.print_exc()
                await self.application.bot.sendMessage(update.effective_chat.id, "Error parsing the format text")
