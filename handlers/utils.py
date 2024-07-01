def get_subcommand_from_command(command: str, text: str):
    length = 1 + len(command)
    if len(text) < length:
        return  None    
    subcommand = text[length:].strip()
    operator = subcommand.split(" ")[0]
    if operator == "":
        return None
    return {"operator":operator,"subcommand":subcommand}