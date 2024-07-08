import logging
import re
from handlers import utils

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers.admin.admin_default_handler import AdminDefaultHandler


class VariableHandler(AdminDefaultHandler):

    COMMAND = 'variable'
    SET_REGEX = re.compile(r'[a-z0-9_]+[\s]+([^,]+,?)+') # "variable val1,val2,val3"
    GET_REGEX = re.compile(r'[a-z0-9_]+') # "variable"
    CLEAR_REGEX = re.compile(r'[a-z0-9_]+') # "variable"
    update = None


    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(VariableHandler, self).__init__(self.COMMAND, dbw, updater)
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
            self.set_variable(subcommand["subcommand"])
        if operator == "get":
            self.get_variable(subcommand["subcommand"])
        if operator == "clear":
            self.clear_variable(subcommand["subcommand"])
        if operator == "list":
            self.list_variables(subcommand["subcommand"])

    def set_variable(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.SET_REGEX.match(processed_command) == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/variable set valname val1,val2,val3")
            return

        variable_name = processed_command.split(" ")[0]
        value = processed_command[len(variable_name):].strip()
        processed_values = value.split(",")
        self.dbw.set_variable_on_group(self.update.effective_chat.id, variable_name, processed_values)
        self.updater.bot.send_message(self.update.effective_chat.id, "Variable saved")

    def clear_variable(self, subcommand: str):
        processed_command = subcommand.strip()[5:].strip()
        if self.CLEAR_REGEX.match(processed_command) == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/variable clear valname")
            return

        variable_name = processed_command
        self.dbw.clean_variable_from_group(self.update.effective_chat.id, variable_name)
        self.updater.bot.send_message(self.update.effective_chat.id, "Variable cleared")

    def get_variable(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.GET_REGEX.match(processed_command) == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/variable get valname")
            return

        variable_name = processed_command
        values = self.dbw.get_variable_on_group(self.update.effective_chat.id, variable_name)
        if values == None:
            self.updater.bot.send_message(self.update.effective_chat.id, "Variable not found")
            return
        value = ""
        for val in values:
            value += val + "\n"
        self.updater.bot.send_message(self.update.effective_chat.id, value)


    def list_variables(self, subcommand: str):
        values = self.dbw.get_all_variables_on_group(self.update.effective_chat.id)
        if values == None or len(values) == 0:
            self.updater.bot.send_message(self.update.effective_chat.id, "No variables found")
            return
        value = ""
        for val in values:
            value += val.name + "\n"
        self.updater.bot.send_message(self.update.effective_chat.id, value)
