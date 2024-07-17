import logging
import re
from handlers import utils
from handlers import constants

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers.admin.admin_default_handler import AdminDefaultHandler


class VariableHandler(AdminDefaultHandler):

    COMMAND = 'variable'
    SET_REGEX = re.compile(r'[a-z0-9_]+[\s]+([^,]+,?)+')  # "variable val1,val2,val3"
    GET_REGEX = re.compile(r'[a-z0-9_]+')  # "variable"
    CLEAR_REGEX = re.compile(r'[a-z0-9_]+')  # "variable"
    update = None

    def __init__(self, dbw: DBWrapper, application: Application):
        super(VariableHandler, self).__init__(self.COMMAND, dbw, application)
        self.application = application

    async def run(self, update: Update, context: CallbackContext):
        self.update = update
        logging.info(self.COMMAND + " command has been called: " + str(update.effective_chat.id))
        if not await self.is_valid(update, context):
            return

        subcommand = utils.get_subcommand_from_command(self.COMMAND, update.message.text)
        if subcommand is None:
            return

        operator = subcommand["operator"]
        logging.debug("Operator: " + operator)
        if operator == "set":
            await self.set_variable(subcommand["subcommand"])
        if operator == "get":
            await self.get_variable(subcommand["subcommand"])
        if operator == "clear":
            await self.clear_variable(subcommand["subcommand"])
        if operator == "list":
            await self.list_variables(subcommand["subcommand"])

    async def set_variable(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.SET_REGEX.match(processed_command) is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/variable set valname val1,val2,val3")
            return

        variable_name = processed_command.split(" ")[0]
        value = processed_command[len(variable_name):].strip()
        processed_values = value.split(",")
        # Validate it don't exceed the maximun
        variables = self.dbw.get_all_variables_on_group(self.update.effective_chat.id)
        # if it already exists it means it's an edit, which is allowed
        exists = False
        for variable in variables:
            if variable.name == variable_name:
                exists = True
                break
        if not exists and len(variables) >= constants.MAX_VARIABLES_PER_GROUP:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "You've reached the max amount of variables that can be created")
            return

        self.dbw.set_variable_on_group(self.update.effective_chat.id, variable_name, processed_values)
        await self.application.bot.sendMessage(self.update.effective_chat.id, "Variable saved")

    async def clear_variable(self, subcommand: str):
        processed_command = subcommand.strip()[5:].strip()
        if self.CLEAR_REGEX.match(processed_command) is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/variable clear valname")
            return

        variable_name = processed_command
        self.dbw.clean_variable_from_group(self.update.effective_chat.id, variable_name)
        await self.application.bot.sendMessage(self.update.effective_chat.id, "Variable cleared")

    async def get_variable(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.GET_REGEX.match(processed_command) is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/variable get valname")
            return

        variable_name = processed_command
        values = self.dbw.get_variable_on_group(self.update.effective_chat.id, variable_name)
        if values is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Variable not found")
            return
        value = ""
        for val in values:
            value += val + "\n"
        await self.application.bot.sendMessage(self.update.effective_chat.id, value)

    async def list_variables(self, subcommand: str):
        values = self.dbw.get_all_variables_on_group(self.update.effective_chat.id)
        if values is None or len(values) == 0:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "No variables found")
            return
        value = ""
        for val in values:
            value += val.name + "\n"
        await self.application.bot.sendMessage(self.update.effective_chat.id, value)
