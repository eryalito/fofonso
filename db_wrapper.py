import logging
import sqlite3


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
