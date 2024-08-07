import logging
import traceback

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application, filters
from handlers.user.custom_handler import CustomMessageHandler
from handlers import utils


class ExclamationHandler(CustomMessageHandler):

    COMMAND = "exclamation"
    MATCH_REGEX = "^![a-z0-9_]+$"

    def __init__(self, dbw: DBWrapper, application: Application):
        super(ExclamationHandler, self).__init__(filters.Regex(self.MATCH_REGEX), self.run, dbw)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        alias = update.message.text[1:].strip()  # remove exclamation mark and strip spaces
        value = self.dbw.get_alias_on_group(update.effective_chat.id, alias)
        text = value.value

        # try to format text and send
        try:
            formatted_text = utils.format_text_for_group(update.effective_chat.id, text, self.dbw)
            await self.application.bot.sendMessage(update.effective_chat.id, formatted_text)
            try:
                self.application.bot.delete_message(update.effective_chat.id, update.effective_message.message_id)
            except Exception:
                logging.debug("Errror deleting message")

        except Exception:
            traceback.print_exc()
            await self.application.bot.sendMessage(update.effective_chat.id, "Error parsing the format text")
        self.pre_command(update, context)
