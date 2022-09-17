from starlette.templating import Jinja2Templates
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from json import JSONDecoder

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

    MAIN_PAGE_CONTENT_LENGTH: list = [
        5,
        5,
        5,
        5,
    ]

    START_BACKGROUND_COLOR: int = 'white'

    PATHS: dict = {
        'MAIN':             'ALL',
        'INFO':             'LOGGED_USERS',
        'ARTICLES':         'LOGGED_USERS',
        'ARTICLES.CREATE':  'LOGGED_USERS',
        'ARTICLE':          'LOGGED_USERS',
        'CHAT':             'LOGGED_USERS',
        'REGISTRATION':     'ALL',
        'LOGIN':            'ALL',
        'ERROR':            'ALL',
        'ADMIN':            'ALL',
        'ADMIN.LOGIN':      'ADMINS',
        'ADMIN.SETTINGS':   'ADMINS'
    }

    LANG_RU: dict = JSONDecoder().decode(open("server/site/content/languages/ru.json", 'r').read())
    LANG_EN: dict = JSONDecoder().decode(open("server/site/content/languages/en.json", 'r').read())