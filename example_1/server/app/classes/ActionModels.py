from random import choice
from fastapi import Response, Request
from fastapi.responses import RedirectResponse

from .Constants import Constants
from .HTMLResponse import HTMLJinjaResponse, HTMLJinjaResponseAdmin

from datetime import datetime

import hashlib

import sqlite3

#  import uuid


class Action:
    answer: str

    def __init__(self) -> None:
        pass


class Main(HTMLJinjaResponse):
    def __init__(self, html: str, response: Response, request: Request) -> None:
        super().__init__(html, response, request)

        if type(self.content) is RedirectResponse:
            pass
        else:
            _lang = Constants.LANG_RU
            if self.is_logged:
                for cookie in request.headers['cookie'].split(';'):
                    if 'id' in cookie.replace(' ', '').split('='):
                        if 'ru' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_RU
                        elif 'en' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_EN

            _articles: list = SQLiteConnection.action('SELECT * FROM main_page_content', [])
            self.content = Constants.TEMPLATES.TemplateResponse(
                    html,
                    {   
                        'request': request, 
                        'logged': self.is_logged,
                        'articles': list(_articles),
                        'rows_length': Constants.MAIN_PAGE_CONTENT_LENGTH,
                        'lang': _lang
                        
                    }
                )


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
        if self.__is_login_and_password_accepted(login, __hash_password):
            # Cant make secure=True because of HTTP (Should be HTTPS or SSL)
            response.set_cookie(key='id', value=self.__get_id(login, __hash_password), httponly=True, samesite='strict')
            response.set_cookie(key='background_color', value=Constants.START_BACKGROUND_COLOR)
            response.set_cookie(key='lang', value='ru')
            # response.delete_cookie(key='id')
        self.answer = path_if_ok

    # def __is_login_accepted(self, login: str) -> bool:
         # return True if len(SQLiteConnection.action('SELECT password FROM users WHERE login = ?0', [login])) > 0 else False

    def __is_login_and_password_accepted(self, login: str, password: str) -> bool:
         return True if len(SQLiteConnection.action('SELECT login FROM users WHERE login = ?0 AND password = ?1', [login, password])) > 0 else False
        
    def __get_id(self, login: str, password: str) -> str:
        return SQLiteConnection.action('SELECT id FROM users WHERE login = ?0 AND password = ?1', [login, password])[0][0]


class AdminLogin(Action):
    def __init__(self, response: Response, login: str, password: str,  path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        # __hash_password: str = MD5.hash(password)
        if self.__is_login_and_password_accepted(login, password):
            # Cant make secure=True because of HTTP (Should be HTTPS or SSL)
            response.set_cookie(key='admin', value=self.__get_id(login, password), httponly=True, samesite='strict')
            # response.delete_cookie(key='id')
            self.answer = path_if_ok
        else:
            self.answer = path_if_not_ok

    # def __is_login_accepted(self, login: str) -> bool:
         # return True if len(SQLiteConnection.action('SELECT password FROM users WHERE login = ?0', [login])) > 0 else False

    def __is_login_and_password_accepted(self, login: str, password: str) -> bool:
         return True if len(SQLiteConnection.action('SELECT login FROM admins WHERE login = ?0 AND password = ?1', [login, password])) > 0 else False
        
    def __get_id(self, login: str, password: str) -> str:
        return SQLiteConnection.action('SELECT admin_id FROM admins WHERE login = ?0 AND password = ?1', [login, password])[0][0]


class AdminLogout(Action):
    def __init__(self, request: Request, response: Response, path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        if self.__is_logged(request):
            response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
            response.delete_cookie(key='admin')
            self.answer = path_if_ok
        else:
            self.answer = path_if_not_ok

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'admin' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False


class AdminSettings(HTMLJinjaResponseAdmin):
    def __init__(self, html: str, response: Response, request: Request) -> None:
        super().__init__(html, response, request)

        if type(self.content) is RedirectResponse:
            pass
        else:
            _lang = Constants.LANG_RU
            if self.is_logged:
                for cookie in request.headers['cookie'].split(';'):
                    if 'admin' in cookie.replace(' ', '').split('='):
                        _admin_id = cookie.replace(' ', '').split('=')[1]
                        if 'ru' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_RU
                        elif 'en' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_EN

                self.content = Constants.TEMPLATES.TemplateResponse(
                        html,
                        {   
                            'request': request, 
                            'logged': self.is_logged,
                            'lang': _lang,
                            'permission': self._get_admin_permission(_admin_id),
                        }
                    )

    def _get_admin_permission(self, id) -> str:
        _permission = SQLiteConnection.action('SELECT permission FROM admins WHERE admin_id = ?0', [id])[0][0]
        if _permission == 0:
            return 'ограниченный'
        elif _permission == 1:
            return 'доверенный'
        elif _permission == 2:
            return 'полный'


class Logout(Action):
    def __init__(self, request: Request, response: Response, path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        if self.__is_logged(request):
            response.delete_cookie(key='id')
            response.delete_cookie(key='background_color')
            response.delete_cookie(key='lang')
            self.answer = path_if_ok
        else:
            self.answer = path_if_not_ok

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False


class Chat:
    def get_messages() -> list:
        return SQLiteConnection.action('SELECT * FROM chat', [])
    
    def add_new_message(response: Response, request: Request, message: str) -> str:
        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        _id = Chat.__get_id(request)
        if _id != False:
            SQLiteConnection.action('INSERT INTO chat (user_id, text, date) VALUES (?0, ?1, ?2)', [_id, message, str(datetime.now())[11:-10]], True)
            return '/chat'
        else:
            return '/chat'

    def __get_id(request: Request) -> any:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return cookie.replace(' ', '').split('=')[1]
            return False
        except KeyError:
            return False


class ArticleCreation(Action):
    def __init__(self, request: Request, response: Response, intro: str, text: str, path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        if self.__is_logged(request):
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    user_id: str = cookie.split('=')[1]
            SQLiteConnection.action('INSERT INTO articles (user_id, intro, text, date) VALUES (?0, ?1, ?2, ?3)', [
                user_id,
                intro,
                text,
                str(datetime.now())[:-7]
            ], True)

            self.answer = path_if_ok
        else:
            self.answer = path_if_not_ok

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False


class Articles(HTMLJinjaResponse):
    def __init__(self, html: str, response: Response, request: Request) -> None:
        super().__init__(html, response, request)

        if type(self.content) is RedirectResponse:
            pass
        else:
            _articles: list = SQLiteConnection.action('SELECT * FROM articles', [])
            _articles.reverse()
            _lang = Constants.LANG_RU
            if self.is_logged:
                for cookie in request.headers['cookie'].split(';'):
                    if 'id' in cookie.replace(' ', '').split('='):
                        if 'ru' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_RU
                        elif 'en' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_EN
            self.content = Constants.TEMPLATES.TemplateResponse(
                    html,
                    {   
                        'request': request, 
                        'logged': self.is_logged,
                        'articles': _articles,
                        'lang': _lang
                    }
                )


class Article(HTMLJinjaResponse):
    def __init__(self, html: str, response: Response, request: Request, id: str) -> None:
        super().__init__(html, response, request)

        if type(self.content) is RedirectResponse:
            pass
        else:
            _article: list = SQLiteConnection.action('SELECT * FROM articles WHERE article_id = ?0', [id])
            _lang = Constants.LANG_RU
            if self.is_logged:
                for cookie in request.headers['cookie'].split(';'):
                    if 'id' in cookie.replace(' ', '').split('='):
                        if 'ru' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_RU
                        elif 'en' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_EN
            self.content = Constants.TEMPLATES.TemplateResponse(
                    html,
                    {   
                        'request': request, 
                        'logged': self.is_logged,
                        'article': _article,
                        'article_meta_like': self._get_like_state(id, Article.__get_id(request)),
                        'article_meta_comments': self._get_comments(id),
                        'user_id': Article.__get_id(request),
                        'lang': _lang
                    }
                )

    def _get_comments(self, article_id: str) -> list:
        _answer: list = SQLiteConnection.action('SELECT * FROM articles_meta WHERE article_id = ?0 AND meta_type = "comment"', [article_id])
        return _answer

    def _get_like_state(self, article_id: str, user_id: str) -> str:
        _answer: list = SQLiteConnection.action('SELECT * FROM articles_meta WHERE article_id = ?0 AND (meta_type = "like" OR meta_type = "dislike")', [article_id])
        if len(_answer) > 0:
            for element in _answer:
                if element[2] == user_id:
                    return element[1]
            return 'None'
        else:
            return 'None'

    def __get_id(request: Request) -> any:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return cookie.split('=')[1]
            return None
        except KeyError:
            return None

    def like(article_id: str, request: Request) -> str:
        _likes: int = int(SQLiteConnection.action('SELECT likes FROM articles WHERE article_id = ?0', [article_id])[0][0])
        SQLiteConnection.action('UPDATE articles SET likes = ?0 WHERE article_id = ?1', [str(_likes + 1), article_id], True)
        Meta.ArticlesMeta.add(
            article_id, 
            'like',
            Article.__get_id(request)
        )

        return f'/articles/{article_id}'

    def leave_comment(article_id: str, request: Request, text: str, response: Response) -> str:
        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        Meta.ArticlesMeta.add(
            article_id, 
            'comment',
            f'{Article.__get_id(request)},{text}'
        )

        return f'/articles/{article_id}'

    def delete_comment(article_id: str, request: Request, comment_info: str) -> str:
        Meta.ArticlesMeta.remove(
            article_id,
            comment_info
        )

        return f'/articles/{article_id}'

    def dislike(article_id: str, request: Request) -> str:
        _dislikes: int = int(SQLiteConnection.action('SELECT dislikes FROM articles WHERE article_id = ?0', [article_id])[0][0])
        SQLiteConnection.action('UPDATE articles SET dislikes = ?0 WHERE article_id = ?1', [str(_dislikes + 1), article_id], True)
        Meta.ArticlesMeta.add(
            article_id, 
            'dislike',
            Article.__get_id(request)
        )

        return f'/articles/{article_id}'

    def remove_like(article_id: str, request: Request) -> str:
        _likes: int = int(SQLiteConnection.action('SELECT likes FROM articles WHERE article_id = ?0', [article_id])[0][0])
        SQLiteConnection.action('UPDATE articles SET likes = ?0 WHERE article_id = ?1', [str(_likes - 1), article_id], True)
        Meta.ArticlesMeta.remove(
            article_id,
            Article.__get_id(request)
        )

        return f'/articles/{article_id}'

    def remove_dislike(article_id: str, request: Request) -> str:
        _dislikes: int = int(SQLiteConnection.action('SELECT dislikes FROM articles WHERE article_id = ?0', [article_id])[0][0])
        SQLiteConnection.action('UPDATE articles SET dislikes = ?0 WHERE article_id = ?1', [str(_dislikes - 1), article_id], True)
        Meta.ArticlesMeta.remove(
            article_id, 
            Article.__get_id(request)
        )

        return f'/articles/{article_id}'

    def delete_article(article_id: str) -> str:
        SQLiteConnection.action('DELETE FROM articles WHERE article_id = ?0', [article_id], True)
        SQLiteConnection.action('DELETE FROM articles_meta WHERE article_id = ?0', [article_id], True)

        return '/articles/'


class Cookie():
    # def __init__(self) -> None:
        # super().__init__()

    def set(response: Response, key: str, value: str, secure: str = 'HALF-FULL'):
        # response.set_cookie(key=key, value=value) if 
        pass

    def delete(response: Response, key: str):
        pass


class Content:
    def update_main_link() -> None:
        SQLiteConnection.action('DELETE FROM main_page_content', [], True)
        _articles: list = SQLiteConnection.action('SELECT * FROM articles', [])
        for lengths in Constants.MAIN_PAGE_CONTENT_LENGTH:
            for length in range(lengths):
                _article: list = choice(_articles)
                SQLiteConnection.action('INSERT INTO main_page_content (article_intro, article_link) VALUES (?0, ?1)', [str(_article), str(_article)], True)


class BackgroundColor(Action):
    def __init__(self, request: Request, response: Response, new_background_color: str, path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        if self.__is_logged(request):
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    response.delete_cookie(key='background_color')
                    response.set_cookie(key='background_color', value=new_background_color)
                    self.answer = path_if_ok
                else:
                    self.answer = path_if_not_ok

            self.answer = path_if_ok
        else:
            self.answer = path_if_not_ok

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False


class Language(Action):
    def __init__(self, request: Request, response: Response, new_language: str, path_if_ok: str, path_if_not_ok: str) -> None:
        super().__init__()

        response.status_code = Constants.STATUS_CODES['FOUND_SO_CHANGE_FROM_POST_TO_GET']
        if self.__is_logged(request):
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    response.delete_cookie(key='lang')
                    response.set_cookie(key='lang', value=new_language)
                    self.answer = path_if_ok
                else:
                    self.answer = path_if_not_ok

            self.answer = path_if_ok
        else:
            self.answer = path_if_not_ok

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False


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


class Meta:
    def __init__(self) -> None:
        pass

    class ArticlesMeta:
        def __init__(self) -> None:
            pass
            
        def add(article_id: str, meta_type: str, meta_storage: str) -> None:
            SQLiteConnection.action('INSERT INTO articles_meta (article_id, meta_type, meta_storage) VALUES (?0, ?1, ?2)', [
                article_id,
                meta_type,
                meta_storage,
            ], True)

        def remove(article_id: str, meta_storage: str) -> None:
            SQLiteConnection.action('DELETE FROM articles_meta WHERE article_id = ?0 AND meta_storage = ?1', [article_id, meta_storage], True)


# Hashing:

class MD5():
    def hash(object: str) -> str:
        return hashlib.md5(object.encode()).hexdigest()

class SHA1():
    def hash(object: str) -> str:
        return hashlib.sha1(object.encode()).hexdigest()
