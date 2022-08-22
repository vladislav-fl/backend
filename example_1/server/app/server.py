"""
    START SERVER: uvicorn server.app.server:server --reload

    THIS SERVER USES COOKIE FOR ALL USER OPERATIONS

    ? Need to do:
        1. Добавить шифрование при добавлении информации в БД - Done

        2. Изменить простые id пользователей на уникальные (возможно хешированные или тп, например - a90Sj)
        3. Максимально обезопасить cookie
        4. Проработать класс Cookie в ActionModels
        5. Реализовать выход с сайта (удаление cookie)
        6. Доделать вход на сайт (Чтобы после добавления cookie на сайта было видно, что пользователь вошел и можно было выйти)

"""

import server.admin.admin as admin

from .classes.HTMLResponse import HTMLBasicResponse, HTMLJinjaResponse
from .classes.ActionModels import Registration, Login

# from ..config.config import Constants
from .classes.Constants import Constants

import sqlite3 as sql

from fastapi import FastAPI, Request, Response, Form, Cookie
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

# Server initialization:
server: FastAPI = FastAPI(debug=True) # routes=Constants.ROUTES

# USER
@server.get('/', response_class=HTMLResponse)
async def root(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    # content: HTMLBasicResponse = HTMLBasicResponse('main.html', response).content
    content: HTMLJinjaResponse = HTMLJinjaResponse('main.html', response, request).content

    print(request.headers)

    # Возврат страницы:
    return content

@server.get('/info', response_class=HTMLResponse)
async def info(response: Response, request: Request) -> HTMLResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('info.html', response, request).content

    # Возврат страницы:
    return content
    
@server.get('/articles', response_class=HTMLResponse)
async def articles(response: Response, request: Request, cookies: str = Cookie(default=None)) -> HTMLResponse:
    # Обработка:
    content: HTMLJinjaResponse = HTMLJinjaResponse('articles.html', response, request).content

    # response.delete_cookie(key='fake_session_2')
    print(request.headers)

    # response.set_cookie(key='__Host-id', value='1')

    # Возврат страницы:
    return content

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

@server.post('/login', response_class=RedirectResponse)
async def registrate(response: Response, login: str = Form(), password: str = Form()) -> RedirectResponse:
    return Login(response, login, password, '/', '/login').answer

# ADMIN
@server.get('/admin')
async def admin(login: str = '', password: str = '') -> dict:
    if login in ['test', '123'] and password in ['test', '123']:
        return {'message': 'OK'}
    else:
        return {'message': 'Wrong login or password'}
