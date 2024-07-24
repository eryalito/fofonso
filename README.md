# Fofonso bot

Fofonso is a bot created to help you with basic tasks in groups. It allows users to at admins, all users, roll dices and more. It has special commands for admins, like format texts, define variables, variables and more.

You can add Fofonso to your group by searching for `@FofonsoBot` on Telegram.

## Commands

### General commands

- `/help`: Show all commands available.
- `/dice`: Roll a dice. You can specify the number of faces.
- `/all`: Mention all users in the group.
- `/admin`: Mention all admins in the group.

### Admin commands

- `/format`: Format a text. You can specify the format and user variables.
- `/variable`: Create, list or delete variables.
- `/alias`: Create, list or delete aliases for specific formats.

## Use cases

### Mention admins

On big groups it can be hard to mention all admins. For example if someone wants to report a problem, they can use the command `/admin` to mention all admins.

### Mention all users

You can use the command `/all` to mention all users in the group. This can be useful to notify all users about something important.

### Create custom texts for users to use

You can use the command `/alias` to create custom texts for users to use. 

- For example, you can create an alias to mention a subset of admins. Just create an alias with the format `@admin1 @admin2 @admin3` and name it `custom_admins`: `/alias set custom_admins @admin1 @admin2 @admin3`. Then users can use the command `!custom_admins` to mention just those admins.

- You can also create an alias to simplify group rules, you can create an alias `rules`: `/alias set rules 1. Do not spam. 2. Be nice. etc`. Then users can use the command `!rules` to get the message.

- You can also create messages with variables. As variables can have multiple values, when formatting a text with a variable, the bot will choose a random value from the variable. For example, you can create a variable `greetings` with the values `Hello`, `Hi`, `Hey`, `Good morning`, `Good afternoon`, `Good evening`. Then you can create an alias `greeting`: `/alias set greeting {greetings}!`. Then users can use the command `!greeting` to get a random greeting.

- You can also create a variable with a single value to create a message that can be updated easily. For example, you can create a variable `welcome` with the value `Welcome to the group!`. Then you can create an alias `welcome`: `/alias set welcome {welcome}`. Then you can update the variable `welcome` to change the message.
