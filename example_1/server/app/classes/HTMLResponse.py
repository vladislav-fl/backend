# from starlette.datastructures import MutableHeaders
from fastapi import Response, Request
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
        self.content = Constants.TEMPLATES.TemplateResponse(
            html, 
            {'request': request, }
        )

        super().__init__(response)

