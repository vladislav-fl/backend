"""
    START SERVER: uvicorn server.app.server:server --reload

    THIS SERVER USES COOKIE FOR ALL USER OPERATIONS

    ? Need to do:
            1. Добавить шифрование при добавлении информации в БД - Done
        2. Изменить простые id пользователей на уникальные (возможно хешированные или тп, например - a90Sj)
        3. Максимально обезопасить cookie
        4. Проработать класс Cookie в ActionModels
            5. Реализовать выход с сайта (удаление cookie) - Done
            6. Доделать вход на сайт (Чтобы после добавления cookie на сайта было видно, что пользователь вошел и можно было выйти) - Done
        7. Создать СМС-рассылку
        8. Добавить удаление комментариев - Done
        9. Добавить удаление статей - Done
        10. Хешировать данные перед отправкой с браузера клиента на сервер, чтобы обезопаситься от HTTP атак
        11. Сделать систему логов

"""

from urllib import request
import server.admin.admin as admin

from .classes.HTMLResponse import HTMLBasicResponse, HTMLJinjaResponse, HTMLJinjaResponseAdmin
from .classes.ActionModels import Registration, Login, Logout, Articles, ArticleCreation, Article, Content, Main, BackgroundColor, Language, Chat, AdminLogin, AdminSettings, AdminLogout

# from ..config.config import Constants
from .classes.Constants import Constants

# import sqlite3 as sql

from fastapi import FastAPI, Request, Response, Form, Cookie
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi_utils.tasks import repeat_every

# Server initialization:
server: FastAPI = FastAPI(debug=True) # routes=Constants.ROUTES

# SERVER REPEATED OPERATIONS
@server.on_event('startup')
@repeat_every(seconds=86400)
async def update_main_link() -> None:
    Content.update_main_link()

# USER
@server.get('/', response_class=HTMLResponse)
async def root(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    # content: HTMLBasicResponse = HTMLBasicResponse('main.html', response).content
    content: Main = Main('main.html', response, request).content

    # Возврат страницы:
    return content

@server.get('/info', response_class=HTMLResponse)
async def info(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('info.html', response, request).content

    # Возврат страницы:
    return content

@server.get('/info/change_background_color', response_class=RedirectResponse) # Change to update
async def change_background_color(response: Response, request: Request, background_color: str) -> HTMLResponse:    
    return BackgroundColor(request, response, background_color, '/', '/info').answer

@server.get('/info/change_language', response_class=RedirectResponse) # Change to update
async def change_language(response: Response, request: Request, language: str) -> HTMLResponse:    
    return Language(request, response, language, '/', '/info').answer

@server.get('/articles', response_class=HTMLResponse)
async def articles(response: Response, request: Request, cookies: str = Cookie(default=None)) -> HTMLResponse:
    # Обработка:
    content: Articles = Articles('articles.html', response, request).content

    # response.delete_cookie(key='fake_session_2')
    # response.set_cookie(key='__Host-id', value='1')

    # Возврат страницы:
    return content

@server.get('/articles/create', response_class=HTMLResponse)
async def articles_create(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('articles.create.html', response, request).content

    # response.delete_cookie(key='fake_session_2')
    # response.set_cookie(key='__Host-id', value='1')

    # Возврат страницы:
    return content

@server.post('/articles/create', response_class=RedirectResponse)
async def article_create(response: Response, request: Request, intro: str = Form(), text: str = Form()) -> HTMLResponse:
    return ArticleCreation(request, response, intro, text, '/articles', '/articles/create').answer

@server.post('/articles/{id}/leave_comment', response_class=RedirectResponse)
async def leave_comment(response: Response, request: Request, id: str, text = Form()) -> HTMLResponse:
    return Article.leave_comment(id, request, text, response)

@server.get('/articles/{id}/delete_comment/{comment_info}', response_class=RedirectResponse) # Сменить на delete
async def delete_comment(response: Response, request: Request, id: str, comment_info: str) -> HTMLResponse:
    return Article.delete_comment(id, request, comment_info)

@server.get('/articles/{id}/like', response_class=RedirectResponse) # Сменить на put
async def article_like(response: Response, request: Request, id: str) -> HTMLResponse:
    return Article.like(id, request)

@server.get('/articles/{id}/dislike', response_class=RedirectResponse) # Сменить на put
async def article_dislike(response: Response, request: Request, id: str) -> HTMLResponse:
    return Article.dislike(id, request)

@server.get('/articles/{id}/delete_like', response_class=RedirectResponse) # Сменить на delete
async def article_delete_like(response: Response, request: Request, id: str) -> HTMLResponse:
    return Article.remove_like(id, request)

@server.get('/articles/{id}/delete_dislike', response_class=RedirectResponse) # Сменить на delete
async def article_delete_dislike(response: Response, request: Request, id: str) -> HTMLResponse:
    return Article.remove_dislike(id, request)

@server.get('/articles/{id}/delete_article', response_class=RedirectResponse) # Сменить на delete
async def delete_article(response: Response, request: Request, id: str) -> HTMLResponse:
    return Article.delete_article(id)

@server.get('/articles/{id}', response_class=HTMLResponse)
async def article(response: Response, request: Request, id: str) -> HTMLResponse:
    # Обработка:
    content: Article = Article('article.html', response, request, id).content

    # response.delete_cookie(key='fake_session_2')
    # response.set_cookie(key='__Host-id', value='1')

    # Возврат страницы:
    return content

@server.get('/chat', response_class=HTMLResponse)
async def chat(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('chat.html', response, request).content

    # Возврат страницы:
    return content

@server.post('/chat', response_class=RedirectResponse)
async def chat_add_new_message(response: Response, request: Request, message: str = Form()) -> RedirectResponse:
    return Chat.add_new_message(response, request, message)

@server.get('/chat/update', response_class=JSONResponse)
async def chat(response: Response, request: Request) -> JSONResponse:
    return {"answer": Chat.get_messages()}

@server.get('/registration', response_class=HTMLResponse)
async def registration_parametres(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('registration.html', response, request).content

    # Возврат страницы:
    return content

@server.post('/registration', response_class=RedirectResponse)
async def registrate(response: Response, login: str = Form(), password: str = Form(), repeat_password: str = Form()) -> RedirectResponse:
    return Registration(response, login, password, repeat_password, '/', '/registration').answer

@server.get('/login', response_class=HTMLResponse)
async def login(response: Response, request: Request) -> HTMLJinjaResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('login.html', response, request).content

    # Возврат страницы:
    return content

@server.get('/error', response_class=HTMLResponse)
async def login(response: Response, request: Request) -> HTMLJinjaResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('error.html', response, request).content

    # Возврат страницы:
    return content

@server.post('/login', response_class=RedirectResponse)
async def registrate(response: Response, login: str = Form(), password: str = Form()) -> RedirectResponse:
    return Login(response, login, password, '/', '/login').answer

@server.get('/logout', response_class=RedirectResponse)
async def registrate(response: Response, request: Request) -> RedirectResponse:
    return Logout(request, response, '/', '/error').answer

# ADMIN
@server.get('/admin', response_class=HTMLResponse)
async def admin(response: Response, request: Request) -> HTMLResponse:
    content: HTMLJinjaResponseAdmin = HTMLJinjaResponseAdmin('admin.html', response, request).content
    print(request.headers)
    # 0 уровень - администрация чата, рассылка
    # 1 уровень - администрация статей, их проверка, удаление и редактирование + 0
    # 2 уровень - самый ахуевший чел + 1 + 0
    return content

@server.post('/admin', response_class=RedirectResponse)
async def admin(response: Response, request: Request, login: str = Form(), password: str = Form()) -> RedirectResponse:
    return AdminLogin(response, login, password, '/admin/settings', '/admin').answer

@server.get('/admin/settings', response_class=HTMLResponse)
async def admin(response: Response, request: Request) -> HTMLResponse:
    print(request.headers)
    content: AdminSettings = AdminSettings('admin.settings.html', response, request).content

    return content

@server.post('/admin/settings', response_class=RedirectResponse)
async def admin(response: Response, request: Request) -> RedirectResponse:
    return AdminLogout(request, response, '/admin', '/admin/settings').answer
