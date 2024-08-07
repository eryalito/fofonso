from typing import List
import logging
import sqlite3
import json


class Variable:
    name: str = ""
    values = []


class Alias:
    name: str = ""
    value: str = ""


class DBWrapper:

    def __init__(self, db_file: str):
        logging.info('Open connection to %s' % db_file)
        self.con = sqlite3.connect(db_file, check_same_thread=False)
        self.con.row_factory = self.dict_factory
        self.__setup()

    def __setup(self):
        logging.info('Setup database')
        cursor = self.con.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS `user` (id bigint, username text)')
        cursor.execute('CREATE TABLE IF NOT EXISTS `user_in_group` (user_id bigint, group_id bigint)')
        cursor.execute('CREATE TABLE IF NOT EXISTS `variable` (group_id bigint, name text, value text)')
        cursor.execute('CREATE TABLE IF NOT EXISTS `alias` (group_id bigint, name text, value text)')
        self.con.commit()

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def add_user(self, id: int, username: str):
        cursor = self.con.cursor()
        logging.debug("Inserting user :user", {"user": username})
        cursor.execute("SELECT id FROM `user` WHERE id=:id", {"id": id})
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `user` VALUES (:id, :username)", {"id": id, "username": username})
        else:
            cursor.execute("UPDATE `user`set username=:username where id=:id", {"id": id, "username": username})
        self.con.commit()

    def get_user(self, id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT id,username FROM `user` WHERE id=:id", {"id": id})
        return cursor.fetchone()

    def add_user_to_group(self, user_id: int, group_id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT user_id,group_id FROM `user_in_group` WHERE user_id=:user_id and group_id=:group_id", {"user_id": user_id, "group_id": group_id})
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `user_in_group` VALUES (:user_id, :group_id)", {"user_id": user_id, "group_id": group_id})
        self.con.commit()

    def get_users_in_group(self, group_id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT id,username FROM `user` left join `user_in_group` on `user`.`id`=`user_in_group`.`user_id` WHERE group_id=:id", {"id": group_id})
        return cursor.fetchall()

    def clean_users_from_group(self, group_id: int):
        cursor = self.con.cursor()
        cursor.execute('DELETE FROM `user_in_group` WHERE group_id=:group_id', {"group_id": group_id})
        self.con.commit()

    def set_variable_on_group(self, group_id: int, variable: str, values):
        cursor = self.con.cursor()
        logging.debug("Inserting variable :variable on group :group", {"variable": variable, "group": group_id})
        obj = Variable()
        obj.name = variable
        obj.values = values
        obj_str = json.dumps(obj.__dict__)
        cursor.execute("SELECT group_id,name FROM `variable` WHERE group_id=:group_id AND name=:name", {"group_id": group_id, "name": variable})
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `variable` VALUES (:group_id, :name, :value)", {"group_id": group_id, "name": variable, "value": obj_str})
        else:
            cursor.execute("UPDATE `variable`set value=:value where group_id=:group_id AND name=:name", {"group_id": group_id, "name": variable, "value": obj_str})
        self.con.commit()

    def get_variable_on_group(self, group_id: int, variable: str) -> List[str]:
        cursor = self.con.cursor()
        cursor.execute("SELECT value FROM `variable` WHERE group_id=:id AND name=:name", {"id": group_id, "name": variable})
        value = cursor.fetchone()
        if value is None:
            return None
        data = json.loads(str(value["value"]))
        obj = Variable()
        obj.name = data["name"]
        obj.values = data["values"]
        return obj.values

    def get_all_variables_on_group(self, group_id: int) -> List[Variable]:
        cursor = self.con.cursor()
        cursor.execute("SELECT value FROM `variable` WHERE group_id=:id", {"id": group_id})
        result = cursor.fetchall()
        if result is None:
            return None
        objs = []
        for value in result:
            data = json.loads(str(value["value"]))
            obj = Variable()
            obj.name = data["name"]
            obj.values = data["values"]
            objs.append(obj)
        return objs

    def clean_variable_from_group(self, group_id: int, variable: str):
        cursor = self.con.cursor()
        cursor.execute('DELETE FROM `variable` WHERE group_id=:group_id AND name=:name', {"group_id": group_id, "name": variable})
        self.con.commit()

    def set_alias_on_group(self, group_id: int, alias: str, value: str) -> None:
        cursor = self.con.cursor()
        logging.debug("Inserting alias :alias on group :group", {"alias": alias, "group": group_id})
        cursor.execute("SELECT group_id,name FROM `alias` WHERE group_id=:group_id AND name=:name", {"group_id": group_id, "name": alias})
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `alias` VALUES (:group_id, :name, :value)", {"group_id": group_id, "name": alias, "value": value})
        else:
            cursor.execute("UPDATE `alias`set value=:value where group_id=:group_id AND name=:name", {"group_id": group_id, "name": alias, "value": value})
        self.con.commit()

    def get_alias_on_group(self, group_id: int, alias: str) -> Alias:
        cursor = self.con.cursor()
        cursor.execute("SELECT value FROM `alias` WHERE group_id=:id AND name=:name", {"id": group_id, "name": alias})
        value = cursor.fetchone()
        if value is None:
            return None
        obj = Alias()
        obj.name = alias
        obj.value = value["value"]
        return obj

    def get_all_aliases_on_group(self, group_id: int) -> List[Alias]:
        cursor = self.con.cursor()
        cursor.execute("SELECT name,value FROM `alias` WHERE group_id=:id", {"id": group_id})
        result = cursor.fetchall()
        if result is None:
            return None
        objs = []
        for value in result:
            obj = Alias()
            obj.name = value["name"]
            obj.value = value["value"]
            objs.append(obj)
        return objs

    def clean_alias_from_group(self, group_id: int, alias: str) -> None:
        cursor = self.con.cursor()
        cursor.execute('DELETE FROM `alias` WHERE group_id=:group_id AND name=:name', {"group_id": group_id, "name": alias})
        self.con.commit()
