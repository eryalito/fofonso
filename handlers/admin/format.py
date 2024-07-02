import logging
import random

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
            variable_names = utils.get_var_names_from_string(text_to_format)
            variable_map = {}

            if len(variable_names) > 0:
                variables_on_group = self.dbw.get_all_variables_on_group(update.effective_chat.id)            
                for variable_name in variable_names:
                    filtered_objects = list(filter(lambda obj: obj.name == variable_name, variables_on_group))
                    result = filtered_objects[0] if filtered_objects else None
                    if result is None:
                        self.updater.bot.send_message(update.effective_chat.id, "Missing variable {var}".format_map({"var": variable_name}))
                        return
                    
                    # When multiple values, randomize the output
                    value = random.choice(result.values)

                    variable_map[variable_name] = value
            
            try:
                formatted_text = text_to_format.format_map(variable_map)
                self.updater.bot.send_message(update.effective_chat.id, formatted_text)
                try:
                    self.updater.bot.delete_message(update.effective_chat.id,update.effective_message.message_id)
                except:
                    logging.debug("Errror deleting message")
                    
            except:
                self.updater.bot.send_message(update.effective_chat.id,"Error parsing the format text")
