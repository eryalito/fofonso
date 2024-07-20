import logging
import re
from handlers import utils
from handlers import constants

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Application

from handlers.admin.admin_default_handler import AdminDefaultHandler


class AliasHandler(AdminDefaultHandler):

    COMMAND = 'alias'
    SET_REGEX = re.compile(r'[a-z0-9_]+[\s].+')  # "alias text"
    GET_REGEX = re.compile(r'[a-z0-9_]+')  # "alias"
    CLEAR_REGEX = re.compile(r'[a-z0-9_]+')  # "alias"
    update = None

    def __init__(self, dbw: DBWrapper, application: Application):
        super(AliasHandler, self).__init__(self.COMMAND, dbw, application)
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
            await self.set_alias(subcommand["subcommand"])
        if operator == "get":
            await self.get_alias(subcommand["subcommand"])
        if operator == "clear":
            await self.clear_alias(subcommand["subcommand"])
        if operator == "list":
            await self.list_alias(subcommand["subcommand"])

    async def set_alias(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.SET_REGEX.match(processed_command) is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/alias set valname val1,val2,val3")
            return

        alias_name = processed_command.split(" ")[0]
        value = processed_command[len(alias_name):].strip()
        # Validate it don't exceed the maximun
        aliases = self.dbw.get_all_aliases_on_group(self.update.effective_chat.id)
        # if it already exists it means it's an edit, which is allowed
        exists = False
        for alias in aliases:
            if alias.name == alias_name:
                exists = True
                break
        if not exists and len(aliases) >= constants.MAX_ALIAS_PER_GROUP:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "You've reached the max amount of aliases that can be created")
            return

        self.dbw.set_alias_on_group(self.update.effective_chat.id, alias_name, value)
        await self.application.bot.sendMessage(self.update.effective_chat.id, "Alias saved")

    async def clear_alias(self, subcommand: str):
        processed_command = subcommand.strip()[5:].strip()
        if self.CLEAR_REGEX.match(processed_command) is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/alias clear valname")
            return

        alias_name = processed_command
        self.dbw.clean_alias_from_group(self.update.effective_chat.id, alias_name)
        await self.application.bot.sendMessage(self.update.effective_chat.id, "Alias cleared")

    async def get_alias(self, subcommand: str):
        processed_command = subcommand.strip()[3:].strip()
        if self.GET_REGEX.match(processed_command) is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Invalid command syntax. Example:\n\n/alias get valname")
            return

        alias_name = processed_command
        value = self.dbw.get_alias_on_group(self.update.effective_chat.id, alias_name)
        if value is None:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "Alias not found")
            return
        await self.application.bot.sendMessage(self.update.effective_chat.id, value.value)

    async def list_alias(self, subcommand: str):
        values = self.dbw.get_all_aliases_on_group(self.update.effective_chat.id)
        if values is None or len(values) == 0:
            await self.application.bot.sendMessage(self.update.effective_chat.id, "No aliases found")
            return
        value = ""
        for val in values:
            value += val.name + "\n"
        await self.application.bot.sendMessage(self.update.effective_chat.id, value)
