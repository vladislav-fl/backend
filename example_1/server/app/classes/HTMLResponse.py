# from starlette.datastructures import MutableHeaders
from fastapi import Response, Request
from fastapi.responses import RedirectResponse

import server.app.classes.ErrorHandler

from .Constants import Constants

class __AbstractResponse:
    content: str

    def __init__(self, response: Response) -> None:
        # Need to add error handler using ErrorHandler:
        try:
            # response.headers['Content-Type'] = 'text/html'
            response.headers['Content-Language'] = 'en-US'
            response.status_code = 200
            #  return self.content
        except:
            pass


# Creates simple HTML template:
class HTMLBasicResponse(__AbstractResponse):
    """Returns response using basic templates:
    
    Keyword arguments:
    argument -- html: str, response: Response
    Return: str
    """
    
    def __init__(self, html: str, response: Response) -> None:
        self.content = open('./server/site/templates/' + html).read().encode()

        super().__init__(response)


# Creates HTML template and fill it with Jinja2 meaning:
class HTMLJinjaResponse(__AbstractResponse):
    def __init__(self, html: str, response: Response, request: Request) -> None:
        self.is_logged: bool = self.__is_logged(request)
        if (self.__is_available_to_get_path(html) == 'LOGGED_USERS' and self.is_logged) or self.__is_available_to_get_path(html) == 'ALL':
            _lang = Constants.LANG_RU
            if self.is_logged:
                for cookie in request.headers['cookie'].split(';'):
                    if 'id' in cookie.replace(' ', '').split('='):
                        if 'ru' in request.headers['cookie'].replace(';', '=').split('='):
                            pass
                        elif 'en' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_EN
            self.content = Constants.TEMPLATES.TemplateResponse(
                html,
                {
                    'request': request, 
                    'logged': self.is_logged,
                    'lang': _lang
                }
            )
        else:
            self.content: RedirectResponse = RedirectResponse('../error')

        super().__init__(response)

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'id' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False

    def __is_available_to_get_path(self, html: str):
        if html[:-5].upper() in Constants.PATHS.keys():
            return Constants.PATHS[html[:-5].upper()]

class HTMLJinjaResponseAdmin(__AbstractResponse):
    def __init__(self, html: str, response: Response, request: Request) -> None:
        self.is_logged: bool = self.__is_logged(request)
        if (self.__is_available_to_get_path(html) == 'ADMINS' and self.is_logged) or self.__is_available_to_get_path(html) == 'ALL':
            _lang = Constants.LANG_RU
            if self.is_logged:
                for cookie in request.headers['cookie'].split(';'):
                    if 'admin' in cookie.replace(' ', '').split('='):
                        if 'ru' in request.headers['cookie'].replace(';', '=').split('='):
                            pass
                        elif 'en' in request.headers['cookie'].replace(';', '=').split('='):
                            _lang = Constants.LANG_EN
            self.content = Constants.TEMPLATES.TemplateResponse(
                html,
                {
                    'request': request, 
                    'logged': self.is_logged,
                    'lang': _lang
                }
            )
        else:
            self.content: RedirectResponse = RedirectResponse('../error')

        super().__init__(response)

    def __is_logged(self, request: Request) -> bool:
        try:
            for cookie in request.headers['cookie'].split(';'):
                if 'admin' in cookie.replace(' ', '').split('='):
                    return True
            return False
        except KeyError:
            return False

    def __is_available_to_get_path(self, html: str):
        if html[:-5].upper() in Constants.PATHS.keys():
            return Constants.PATHS[html[:-5].upper()]
