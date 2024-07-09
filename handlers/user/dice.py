import logging
import random
import re

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers.user.custom_handler import CustomHandler


class DiceHandler(CustomHandler):

    COMMAND = 'dice'
    COMMAND_LENGTH = len(COMMAND) + 1  # /COMMAND
    REGEX = re.compile(r'[\d]+ [\d]+')  # "min max"
    DICE_MIN = 1
    DICE_MAX = 6

    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(DiceHandler, self).__init__(self.COMMAND, self.run, dbw)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + ' command has been called: ' + str(update.effective_chat.id))
        self.pre_command(update, context)
        command = update.message.text
        subcommand = command[self.COMMAND_LENGTH:].strip()
        min = self.DICE_MIN
        max = self.DICE_MAX
        if self.REGEX.match(subcommand) is not None:
            arr = subcommand.split(" ")
            min_string = arr[0]
            max_string = arr[1]
            min = int(min_string)
            max = int(max_string)
            if min >= max:
                self.updater.bot.send_message(update.effective_chat.id, "Min must be lower then Max")
                return
        rand = random.randint(min, max)
        self.updater.bot.send_message(update.effective_chat.id, str(rand))
