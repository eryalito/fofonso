import logging
import re
from handlers import utils

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers.admin.admin_default_handler import AdminDefaultHandler


class AliasHandler(AdminDefaultHandler):

    COMMAND = 'alias'
    SET_REGEX = re.compile(r'[a-z0-9-]+[\s].+') # "alias text"
    GET_REGEX = re.compile(r'[a-z0-9-]+') # "alias"
    CLEAR_REGEX = re.compile(r'[a-z0-9-]+') # "alias"
    update = None


    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(AliasHandler, self).__init__(self.COMMAND, dbw, updater)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        self.update = update
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if not self.is_valid(update, context):
            return

        subcommand = utils.get_subcommand_from_command(self.COMMAND, update.message.text)
        if subcommand is None:
            return
        
        operator = subcommand["operator"]
        logging.debug("Operator: " + operator)
        if operator == "set":
            self.set_alias(subcommand["subcommand"])
        if operator == "get":
            self.get_alias(subcommand["subcommand"])
        if operator == "clear":
            self.clear_alias(subcommand["subcommand"])
        if operator == "list":
            self.list_alias(subcommand["subcommand"])

    def set_alias(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.SET_REGEX.match(processed_command) == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/alias set valname val1,val2,val3")
            return

        alias_name = processed_command.split(" ")[0]
        value = processed_command[len(alias_name):].strip()
        self.dbw.set_alias_on_group(self.update.effective_chat.id, alias_name, value)
        self.updater.bot.send_message(self.update.effective_chat.id, "Alias saved")

    def clear_alias(self, subcommand: str):
        processed_command = subcommand.strip()[5:].strip()
        if self.CLEAR_REGEX.match(processed_command) == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/alias clear valname")
            return

        alias_name = processed_command
        self.dbw.clean_alias_from_group(self.update.effective_chat.id, alias_name)
        self.updater.bot.send_message(self.update.effective_chat.id, "Alias cleared")

    def get_alias(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.GET_REGEX.match(processed_command) == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/alias get valname")
            return

        alias_name = processed_command
        value = self.dbw.get_alias_on_group(self.update.effective_chat.id, alias_name)
        if value == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Alias not found")
            return
        self.updater.bot.send_message(self.update.effective_chat.id, value.value)


    def list_alias(self, subcommand: str):
        values = self.dbw.get_all_aliases_on_group(self.update.effective_chat.id)
        if values == None or len(values) == 0:
            self.updater.bot.send_message(self.update.effective_chat.id, "No aliases found")
            return
        value = ""
        for val in values:
            value += val.name + "\n"
        self.updater.bot.send_message(self.update.effective_chat.id, value)
