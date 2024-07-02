import string

def get_subcommand_from_command(command: str, text: str):
    length = 1 + len(command)
    if len(text) < length:
        return  None    
    subcommand = text[length:].strip()
    operator = subcommand.split(" ")[0]
    if operator == "":
        return None
    return {"operator":operator,"subcommand":subcommand}

# Return an array with the list of variables on a text to be formatted
def get_var_names_from_string(text: str):
    formatter = string.Formatter()

    return [field_name for _, field_name, _, _ in formatter.parse(text) if field_name]