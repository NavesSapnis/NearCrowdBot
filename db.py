import sqlite3
import parseMoney


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_my_acc(self, user_id, name, procent,personal_name):
        self.cursor.execute("INSERT INTO `accounts` (`user_id`,`name`, `procent`, `personal_name`) VALUES (?, ?, ?, ?)",
            (user_id,
            name,
            procent,
            personal_name))
        return self.conn.commit()


    def remove_my_acc(self, user_id,personal_name):
        self.cursor.execute("DELETE FROM `accounts` WHERE `user_id` = ? AND  `personal_name` = ? ",(user_id,personal_name,))
        return self.conn.commit()

    def add_worker_acc(self, user_id, name, procent,personal_name,wallet,keys):
        self.cursor.execute("INSERT INTO `worker_acc` (`user_id`,`name`, `procent`, `personal_name`, `wallet`,`keys`) VALUES (?, ?, ?, ?, ?,?)",
            (user_id,
            name,
            procent,
            personal_name,
            wallet,
            keys))
        return self.conn.commit()


    def name_check(self,personal_name):
        result = self.cursor.execute("SELECT `user_id` FROM `accounts` WHERE `personal_name` = ?", (personal_name,))
        return bool(len(result.fetchall()))

#klass
    def get_my_acc(self, user_id):
        result = self.cursor.execute("SELECT `personal_name` FROM `accounts` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()

    def get_acc(self, personal_name,user_id):
        acc = self.cursor.execute("SELECT `name` FROM `accounts` WHERE `personal_name` = ? AND `user_id` = ?", (personal_name,user_id,))
        return acc.fetchone()

    def get_procent(self, personal_name,user_id):
        procent = self.cursor.execute("SELECT `procent` FROM `accounts` WHERE `personal_name` = ? AND `user_id` = ?", (personal_name,user_id,))
        return procent.fetchone()


    def name_check2(self,personal_name):
        result = self.cursor.execute("SELECT `user_id` FROM `worker_acc` WHERE `personal_name` = ?", (personal_name,))
        return bool(len(result.fetchall()))

    def get_worker_acc(self, user_id):
        result = self.cursor.execute("SELECT `personal_name` FROM `worker_acc` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()

    def get_acc2(self, personal_name,user_id):
        acc = self.cursor.execute("SELECT `name` FROM `worker_acc` WHERE `personal_name` = ? AND `user_id` = ?", (personal_name,user_id,))
        return acc.fetchone()

    def get_procent2(self, personal_name,user_id):
        procent = self.cursor.execute("SELECT `procent` FROM `worker_acc` WHERE `personal_name` = ? AND `user_id` = ?", (personal_name,user_id,))
        return procent.fetchone()


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()