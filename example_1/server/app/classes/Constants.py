from starlette.templating import Jinja2Templates
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

class Constants:
    STATUS_CODES: dict = {
        'FOUND_SO_CHANGE_FROM_POST_TO_GET': 302, # To reach from POST method to GET
    }

    SQLiteURL = './server/data/db/db.sqlite'

    TEMPLATES = Jinja2Templates(directory='./server/site/templates/')

    # async def __homepage(request): return Constants.TEMPLATES.TemplateResponse('index.html', {'request': request})
    # ROUTES = [
    #     Route('/', endpoint=__homepage),
    #     Mount('/static', StaticFiles(directory='/'), name='static')
    # ]