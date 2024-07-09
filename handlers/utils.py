import random
import string
from db_wrapper import DBWrapper


def get_subcommand_from_command(command: str, text: str):
    length = 1 + len(command)
    if len(text) < length:
        return None
    subcommand = text[length:].strip()
    operator = subcommand.split(" ")[0]
    if operator == "":
        return None
    return {"operator": operator, "subcommand": subcommand}


# Return an array with the list of variables on a text to be formatted
def get_var_names_from_string(text: str):
    formatter = string.Formatter()

    return [field_name for _, field_name, _, _ in formatter.parse(text) if field_name]


def format_text_for_group(group_id: str, text: str, dbw: DBWrapper) -> str:
    variable_names = get_var_names_from_string(text)
    variable_map = {}

    if len(variable_names) > 0:
        variables_on_group = dbw.get_all_variables_on_group(group_id)
        for variable_name in variable_names:
            filtered_objects = list(filter(lambda obj: obj.name == variable_name, variables_on_group))
            result = filtered_objects[0] if filtered_objects else None
            if result is None:
                return "Missing variable {var}".format_map({"var": variable_name})

            # When multiple values, randomize the output
            value = random.choice(result.values)
            variable_map[variable_name] = value

    return text.format_map(variable_map)
