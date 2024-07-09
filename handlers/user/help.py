import logging
from handlers import utils

from db_wrapper import DBWrapper
from telegram import Update
from telegram.ext import CallbackContext, Updater

from handlers.user.custom_handler import CustomHandler


class HelpHandler(CustomHandler):

    COMMAND = 'help'
    TEXT = '''
Hey, I'm Fofonso!

I am a bot designed to assist you with group management and basic tasks.

Here are some of the available commands:

/help - Display this help message
/start - Start interacting with the bot, welcome message

General Commands
/dice [min] [max] - Throw a dice between min and max value (1 and 6 if not provided)

Group Commands
/admins - Send a message atting all of the admins of the group
/all - Send a message atting all of the users on the group
!<name> - Exclamation command invokes an alias text. More into on /help !

Group Admin Commands
/reset - Reset the user list of the group (Use when a user left the group or change the @)
/variable <list|set|get|clear> [name] [value] - Handle variable values
/format <text> - Format the given text, allows variables usage.
/alias <list|set|get|clear> [name] [value] - Handle alias values

For more information on each command, type the command /help <command>.

Please use the /help command in a private chat.

Check me out at /github
'''

    EXPLANATIONS = {
        "reset": '''
[Group Only - Admin]

It reset the list of users of a chat used on the /all command.

The list of users on the /all command are cached the first time they send a message to the bot. When a user leaves the group or change its username the list is not updated. Therefore you might want to clear the list of users so it's updated.

Note: Currently this is the behaviour but it could change over time so make sure to run /help reset before using it.
        ''',
        "all": '''
[Group Only]

Send a message atting all of the users that have send a message since the bot was added to the group or from the last /reset command.

Only users with @ configured as public will be atted.
        ''',
        "admins": '''
[Group Only]

Send a message atting all of the admins of the group.

Only admins with @ configured as public will be atted.
        ''',
        "dice": '''
[General]

Send a random number between two values.

Usage:
/dice [min] [max]

Note: If values are not provided by default it would generate a number between 1 and 6
        ''',
        "variable": '''
[Group Only - Admin]

Handle variables on the group. a variable is a key-value element. The value can be a list of different texts if separated by comma. Names of the variables can only be lowercase, numbers or underscore (_). Values can be any text that not contains a comma (,).

This command have a set of subcommands to properly handle variables.

/variable list - List all of the variables on the group. Just the list of the names

/variable get <name> - Gets the value(s) of the variable with that name. If the value contains multiple texts it will be shown one per line.

/variable clear <name> - Deletes the variable with that name

/variable set <name> <value> - Set the value for the variable with that name. For multiple values separate them by comma (e.g. /variable set <name> <val1>,<val2>)

        ''',
        "format": '''
[Group Only - Admin]

Format the given text and send it back to the chat as a message. It allow using variable values.

Example:

/format My message - The message would be "My message"

Using variables:

Supposing the variable "var1" has the value "value1"

/format Value {var1} - The message would be "Value value1"

Note: When the variable contains multiple values a random value would be selected.
        ''',
        "alias": '''
[Group Only - Admin]

Handle alias on the group. An alias is a key-value element same as variables. Names of the alias can only be lowercase, numbers or underscore (_). Values can be any text.
Aliases are used on the exclamation command so any user can invoke the value as it was the text on the /format command, it allows using variables.

Example: the variable "var" exists with value "value1". Create the alias "my_alias" with value "Test: {var}" (/alias set my_alias Test: {var}). To render the alias use the exclamation with the alias name (!my_alias), it will print the same as running /format Test: {var} (Test: value1)

This command have a set of subcommands to properly handle variables.

/alias list - List all of the alias on the group. Just the list of the names

/alias get <name> - Gets the value(s) of the alias with that name

/alias clear <name> - Deletes the alias with that name

/alias set <name> <value> - Set the value for the alias with that name

        ''',
        "!": '''
[Group Only]

The exclamation command works similar to the /format one, but text to format can't be provided. An admin must define an alias naming a text to format so it can be used using the exclamation operator.

To format an alias use the exclamation alongside the alias name: !<aliasname>

Example: 

1. Admin create the equivalent alias for a format text /alias set my_name Format text!
2. All users can use the !my_name, which is equivalent to "/format Format text!" but without admin permissions.

        '''
    }

    def __init__(self, dbw: DBWrapper, updater: Updater):
        super(HelpHandler, self).__init__(self.COMMAND, self.run, dbw)
        self.updater = updater

    def run(self, update: Update, context: CallbackContext):
        logging.info(self.COMMAND + ' command has been called: ' + str(update.effective_chat.id))
        self.pre_command(update, context)
        subcommand = utils.get_subcommand_from_command(self.COMMAND, update.message.text)
        if subcommand is None:
            self.updater.bot.send_message(update.effective_chat.id, self.TEXT)
        elif subcommand["operator"] in self.EXPLANATIONS.keys():
            self.updater.bot.send_message(update.effective_chat.id, self.EXPLANATIONS.get(subcommand["operator"]))
        else:
            self.updater.bot.send_message(update.effective_chat.id, "Not recognized command. Use /help to get more info.")
