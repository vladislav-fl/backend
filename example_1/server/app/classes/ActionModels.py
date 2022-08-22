from fastapi import Response
from .Constants import Constants

import hashlib

import sqlite3

#  import uuid


class Action:
    answer: any

    def __init__(self) -> None:
        pass


class Registration(Action):
    def __init__(self, response: Response, login: str, password: str, repeat_password: str, path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        if password == repeat_password:
            if not self.__check_for_login_repeats(login):
                SQLiteConnection.action('INSERT INTO users (login, password) VALUES (?0, ?1)', 
                                            [login, MD5.hash(password)], 
                                            True)
                self.answer = path_if_ok
            else:
                self.answer = path_if_not_ok
        else:
            self.answer = path_if_not_ok

    def __check_for_login_repeats(self, login: str) -> bool:
        return True if len(SQLiteConnection.action('SELECT password FROM users WHERE login = ?0', [login])) > 0 else False


class Login(Action):
    def __init__(self, response: Response, login: str, password: str,  path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        __hash_password: str = MD5.hash(password)
        # print(self.__is_login_accepted(login))
        # print(self.__is_password_accepted(__hash_password))
        if self.__is_login_and_password_accepted(login, __hash_password):
            # Cant make secure=True because of HTTP (Should be HTTPS or SSL)
            response.set_cookie(key='id', value=self.__get_id(login, __hash_password), httponly=True, samesite='strict')
        self.answer = path_if_ok

    # def __is_login_accepted(self, login: str) -> bool:
         # return True if len(SQLiteConnection.action('SELECT password FROM users WHERE login = ?0', [login])) > 0 else False

    def __is_login_and_password_accepted(self, login: str, password: str) -> bool:
         return True if len(SQLiteConnection.action('SELECT login FROM users WHERE login = ?0 AND password = ?1', [login, password])) > 0 else False
        
    def __get_id(self, login: str, password: str) -> str:
        return SQLiteConnection.action('SELECT id FROM users WHERE login = ?0 AND password = ?1', [login, password])[0][0]


class Cookie():
    # def __init__(self) -> None:
        # super().__init__()

    def set(response: Response, key: str, value: str, secure: str = 'HALF-FULL'):
        # response.set_cookie(key=key, value=value) if 
        pass

    def delete(response: Response, key: str):
        pass


class SQLiteConnection():
    # def __init__(self, ) -> None:
        # self.cursor = sqlite3.connect(Constants.SQLiteURL).cursor()
    
    @staticmethod
    def action(command: str, values: list, is_need_to_commit: bool = False) -> list:
        __command = SQLiteConnection.__write_values_into_command(command, values)
        __connection = SQLiteConnection.__connect()
        __cursor = SQLiteConnection.__get_cursor(__connection)
        __answer = __cursor.execute(__command).fetchall()
        __answer = SQLiteConnection.__commit(__answer, __connection, is_need_to_commit)
        SQLiteConnection.__close_connection(__cursor, __connection)

        return __answer

    # Zero srep - replace special signs (0, 1, 2...) with values:
    def __write_values_into_command(__command: str, __values: list) -> str:
        for i in range(len(__values)):
            __command = __command.replace('?' + str(i), '"' + __values[i] + '"')
        return __command

    # First step - make connection to db:
    def __connect() -> sqlite3.Connection:
        return sqlite3.connect(Constants.SQLiteURL)

    # Second step - get cursor from db:
    def __get_cursor(__connection: sqlite3.Connection) -> sqlite3.Cursor:
        return __connection.cursor()

    # Third optional step - commit changes if its not read operation:
    def __commit(__answer: list, __connection: sqlite3.Connection, __need: bool) -> list:
        if __need:
            __connection.commit()
            __answer = [True]
        return __answer

    # Final step - close connection to cursor and database:
    def __close_connection(__cursor: sqlite3.Cursor, __connection: sqlite3.Connection) -> None:
        __cursor.close()
        __connection.close()


# Hashing:

class MD5():
    def hash(object: str) -> str:
        return hashlib.md5(object.encode()).hexdigest()

class SHA1():
    def hash(object: str) -> str:
        return hashlib.sha1(object.encode()).hexdigest()
